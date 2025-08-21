# ArtDept MCP Server - Technical Specification

This document provides a comprehensive technical specification for the ArtDept MCP Server, including architecture details, implementation specifics, and protocol compliance.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [MCP Protocol Implementation](#mcp-protocol-implementation)
- [OpenAI API Integration](#openai-api-integration)
- [Tool Specifications](#tool-specifications)
- [Prompt Engineering Strategy](#prompt-engineering-strategy)
- [Error Handling](#error-handling)
- [Security Considerations](#security-considerations)
- [Performance Characteristics](#performance-characteristics)
- [Future Enhancements](#future-enhancements)

## Architecture Overview

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  ArtDept Server  │◄──►│   OpenAI API    │
│  (Claude, etc.) │    │                  │    │   (DALL-E 3)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Local Storage  │
                       │ (Creative dirs) │
                       └─────────────────┘
```

### Core Architecture

The ArtDept MCP Server is built using:

- **Framework**: Python MCP SDK (mcp>=1.0.0)
- **Image Generation**: OpenAI API with `gpt-image-1` model
- **Response Format**: Base64-encoded JSON (no URL downloads)
- **Transport**: STDIO-based communication
- **Async Runtime**: Python asyncio
- **Dependency Management**: UV script runner
- **File I/O**: Pathlib for direct base64 decoding and saving

### Key Design Principles

1. **Separation of Concerns**: Distinct prompt builders for each tool type
2. **Async-First**: All I/O operations are asynchronous
3. **Error Resilience**: Comprehensive error handling with partial success support
4. **Type Safety**: Pydantic models for data validation
5. **Configurability**: Environment-based configuration

## MCP Protocol Implementation

### Protocol Compliance

The server implements MCP v1.0 with the following capabilities:

- **Tools**: 6 creative design tools
- **Transport**: STDIO transport only
- **Initialization**: Standard MCP initialization handshake
- **Error Handling**: MCP-compliant error responses

### Tool Registration

```python
@server.list_tools()
async def list_tools() -> List[Tool]:
    """Returns all 6 available tools with JSON Schema validation."""
```

Each tool is registered with:
- **Name**: Unique tool identifier
- **Description**: Human-readable purpose
- **Input Schema**: JSON Schema for parameter validation

### Tool Execution

```python
@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Dispatches tool calls to appropriate handlers."""
```

All tool responses follow the standard MCP format:
- **Type**: TextContent
- **Content**: JSON-serialized ImageGenerationResult

### Message Format

Tool responses are structured JSON:

```python
class ImageGenerationResult(BaseModel):
    success: bool                    # Operation success status
    message: str                     # Human-readable summary
    paths: List[str] = []           # Generated file paths
    errors: List[str] = []          # Error messages if any
```

## OpenAI API Integration

### API Client Configuration

```python
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

### Image Generation Parameters

**Fixed Parameters:**
- **Model**: `gpt-image-1` (latest generation model)
- **Quality**: `standard` (cost-optimized)
- **Response Format**: `b64_json` (base64 encoded)
- **N**: 1 (single image per request)

**Variable Parameters:**
- **Prompt**: Tool-specific enhanced prompts
- **Size**: Tool and user-specified dimensions
- **Variations**: Achieved through multiple API calls

### Supported Image Sizes

- `1024x1024` - Square format (logos, icons)
- `1024x1536` - Portrait format (mobile wireframes)
- `1536x1024` - Landscape format (desktop wireframes, design systems)

### Rate Limiting

The server implements basic error handling for rate limits but does not include built-in retry logic. Clients should handle rate limit responses appropriately.

### Implementation Constants

The server uses the following fixed constants:

```python
# Model and quality settings
MODEL = "gpt-image-1"
QUALITY = "standard" 
RESPONSE_FORMAT = "b64_json"

# Image sizes by tool
WIREFRAME_SIZES = {
    "desktop": "1536x1024",
    "mobile": "1024x1536"
}
DESIGN_SYSTEM_SIZE = "1536x1024"
LOGO_SIZE = "1024x1024" 
ICON_SIZE = "1024x1024"
ILLUSTRATION_SIZES = ["1024x1024", "1536x1024", "1024x1536"]
PHOTO_SIZES = ["1024x1024", "1536x1024", "1024x1536"]

# File formats by tool
WIREFRAME_FORMAT = ".jpg"
DESIGN_SYSTEM_FORMAT = ".jpg"
LOGO_FORMAT = ".png"
ICON_FORMAT = ".png" 
ILLUSTRATION_FORMAT = ".png"
PHOTO_FORMAT = ".jpg"
```

### Base64 Image Processing

```python
async def save_base64_image(b64_data: str, filepath: Path) -> bool:
    """Save base64 encoded image data to filesystem."""
```

Process:
1. Decode base64 string to binary data
2. Create parent directories if needed
3. Write binary content to file
4. Log success/failure

This approach eliminates the need for HTTP downloads and provides faster, more reliable image saving.

## Tool Specifications

### 1. new_wireframe

**Purpose**: Generate UI/UX wireframes with device-specific optimizations.

**Implementation Details:**
- **Prompt Builder**: `build_wireframe_prompt()`
- **Device Handling**: Automatic size selection based on device type
- **Multi-Device**: Sequential generation for "both" option
- **File Format**: JPEG (smaller size for wireframes)

**Size Logic:**
```python
devices_to_generate = []
if device == "both":
    devices_to_generate = [("desktop", "1536x1024"), ("mobile", "1024x1536")]
elif device == "desktop":
    devices_to_generate = [("desktop", "1536x1024")]
elif device == "mobile":
    devices_to_generate = [("mobile", "1024x1536")]
```

### 2. new_designsystem

**Purpose**: Create comprehensive design system presentations.

**Implementation Details:**
- **Prompt Builder**: `build_design_system_prompt()`
- **Type Specialization**: Brand, UI, UX-specific prompting
- **Color Integration**: Dynamic color specification handling
- **Variation Strategy**: Sequential generation with variation prompts

**Type Handling:**
```python
type_context = {
    "brand": "brand design system with logo variations, color palette, typography, and brand elements",
    "ui": "UI component design system with buttons, forms, cards, navigation, and interface elements",
    "ux": "UX design system with user flows, interaction patterns, and experience guidelines"
}
```

### 3. new_logo

**Purpose**: Professional logo generation with scalable design principles.

**Implementation Details:**
- **Prompt Builder**: `build_logo_prompt()`
- **Scalability Focus**: Prompts emphasize vector-style design
- **Color Specification**: Flexible color input handling
- **Format**: PNG for transparency support (note: transparency may not be supported by gpt-image-1)
- **Size**: Fixed 1024x1024 square format

### 4. new_icon

**Purpose**: UI/UX icon generation with consistency focus.

**Implementation Details:**
- **Prompt Builder**: `build_icon_prompt()`
- **Consistency Emphasis**: "Suitable for icon sets" prompting
- **Scalability**: Multiple size readability requirements
- **Format**: PNG for transparency (note: transparency may not be supported by gpt-image-1)
- **Size**: Fixed 1024x1024 square format

### 5. new_illustration

**Purpose**: Custom illustration generation with artistic flexibility.

**Implementation Details:**
- **Prompt Builder**: `build_illustration_prompt()`
- **Style Flexibility**: Wide range of artistic styles supported
- **Size Options**: Three aspect ratio choices (1024x1024, 1536x1024, 1024x1536)
- **Format**: PNG for transparency and quality (note: transparency may not be supported by gpt-image-1)

### 6. new_photo

**Purpose**: Photorealistic image generation.

**Implementation Details:**
- **Prompt Builder**: `build_photo_prompt()`
- **Realism Focus**: Professional photography emphasis
- **Lighting/Composition**: Technical photography terms
- **Size Options**: Three aspect ratio choices (1024x1024, 1536x1024, 1024x1536)
- **Format**: JPEG for photographic content

## Prompt Engineering Strategy

### Hierarchical Prompting

Each tool uses a structured prompt format:

1. **Requirements Section**: Technical specifications
2. **Style Section**: Aesthetic guidelines
3. **Format Section**: Output format requirements
4. **User Section**: Injected user prompt
5. **Quality Section**: Professional standards

### Example Structure (Logo):

```python
def build_logo_prompt(user_prompt: str, style: str, colors: str) -> str:
    return f"""Design a professional logo:

REQUIREMENTS:
- Style: {style if style else 'modern, scalable logo design'}
- Colors: {color_spec}
- Format: Clean vector-style design (note: transparent background may not be supported)
- Versatility: Works at different sizes
- Simplicity: Clear and memorable
- Professional quality
- Centered composition
- Adequate padding around the logo

USER SPECIFICATION:
{user_prompt}

Create a distinctive, professional logo that would work across various media."""
```

### Prompt Enhancement Strategies

1. **Context Setting**: Clear medium and purpose specification
2. **Technical Requirements**: Format, size, and quality standards
3. **Style Guidance**: Aesthetic direction and constraints
4. **Professional Standards**: Quality and usability requirements
5. **User Integration**: Natural language user input preservation

### Variation Generation

For multiple variations (n > 1), prompts are enhanced with:
- Unique variation indicators
- Sequential numbering
- Distinctiveness requirements

Example: `f"{enhanced_prompt}\n\nUnique variation {i+1} of {n}"`

## Error Handling

### Error Categories

1. **Environment Errors**: Missing API key, configuration issues
2. **API Errors**: OpenAI rate limits, quota exceeded, service unavailable
3. **I/O Errors**: File system permissions, disk space, network issues
4. **Validation Errors**: Invalid parameters, unsupported sizes

### Error Response Strategy

**Partial Success Support**: Operations can succeed partially (some images generated, others failed).

```python
class ImageGenerationResult(BaseModel):
    success: bool                    # True if any images generated
    message: str                     # Summary of operation
    paths: List[str] = []           # Successfully generated files
    errors: List[str] = []          # Specific error messages
```

### Error Logging

Comprehensive logging at multiple levels:
- **INFO**: Successful operations and server status
- **ERROR**: Failed operations with details
- **DEBUG**: Detailed execution traces

### Exception Hierarchy

```python
try:
    # Image generation logic
except OpenAIError as e:
    # OpenAI API specific errors
except httpx.RequestError as e:
    # Network/download errors
except Exception as e:
    # General fallback
```

## Security Considerations

### API Key Protection

- **Environment Variable**: API key stored in environment
- **No Hardcoding**: No API keys in source code
- **Client Isolation**: Each client provides own API key

### Input Validation

- **Schema Validation**: JSON Schema enforcement for all parameters
- **Path Validation**: Safe file path construction
- **Content Filtering**: Relies on OpenAI's content policy

### File System Security

- **Directory Isolation**: Files saved to configured directories only
- **Path Sanitization**: Use of pathlib for safe path construction
- **Permission Handling**: Graceful handling of permission errors

## Performance Characteristics

### Latency Considerations

**Typical Response Times:**
- Single image: 10-30 seconds
- Multiple variations: 30-120 seconds (sequential)
- Wireframes (both devices): 20-60 seconds

**Bottlenecks:**
1. OpenAI API generation time
2. Base64 decoding and file writing
3. Sequential image generation for variations

### Throughput Limitations

- **Sequential Processing**: One image at a time per tool call
- **API Limits**: OpenAI account-specific rate limits
- **No Caching**: Each request generates new images

### Resource Usage

- **Memory**: Minimal (base64 strings held temporarily during decoding)
- **Disk**: Direct local storage, no temporary files
- **Network**: Bandwidth for API requests only (base64 responses ~1.3x image size)

## Future Enhancements

### Planned Improvements

1. **Caching System**:
   - Content-based caching of generated images
   - Prompt similarity detection
   - Cache invalidation strategies

2. **Batch Processing**:
   - Parallel image generation where possible
   - Improved throughput for multiple variations

3. **Quality Options**:
   - HD quality option for premium use cases
   - Quality/cost trade-off controls

4. **Advanced Prompting**:
   - Style transfer capabilities
   - Reference image support
   - Iterative refinement

5. **Metadata Enhancement**:
   - EXIF data with generation parameters
   - Prompt preservation in metadata
   - Version tracking

6. **Format Extensions**:
   - SVG output for logos and icons
   - PDF output for design systems
   - Multiple format generation

## Testing Framework

### Test Suite Coverage

The server includes a comprehensive test suite (`test_server.py`) with 15 test cases covering:

**Core Functionality Tests:**
- `test_generate_wireframe_desktop` - Desktop wireframe generation
- `test_generate_wireframe_mobile` - Mobile wireframe generation  
- `test_generate_wireframe_both_devices` - Multi-device wireframe generation
- `test_generate_design_system` - Design system variations
- `test_generate_logo` - Logo generation with variations
- `test_generate_icon` - Icon generation
- `test_generate_illustration` - Custom size illustration generation
- `test_generate_photo` - Photo generation with custom size

**Parameter Validation Tests:**
- `test_parameter_validation_n_constraint` - Validates n parameter limits (1-4)

**Error Handling Tests:**
- `test_api_error_handling` - OpenAI API failure scenarios
- `test_file_save_error_handling` - File system error scenarios

**Base64 Processing Tests:**
- `test_save_base64_image_success` - Base64 decoding and file saving
- `test_save_base64_image_directory_creation` - Directory creation

**Prompt Engineering Tests:**
- `test_prompt_builders` - All prompt building functions

**Integration Tests:**
- `test_tool_call_routing` - MCP tool routing and unknown tool handling

### Test Execution

```bash
# Run test suite
uv run test_server.py
# or
python test_server.py
```

### Test Data

Tests use mock base64 image data representing a single-pixel PNG:
```python
MOCK_B64_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
```

### Technical Debt

1. **Error Recovery**: Implement retry logic with exponential backoff
2. **Configuration**: External configuration file support
3. **Logging**: Structured logging with correlation IDs

### Integration Opportunities

1. **Design Tools**: Figma, Sketch plugin integration
2. **Version Control**: Git-based asset versioning
3. **Asset Management**: DAM system integration
4. **Collaboration**: Real-time sharing and feedback

### Scalability Considerations

For production deployment:

1. **API Key Pool**: Multiple API key rotation
2. **Load Balancing**: Multiple server instances
3. **Queue System**: Asynchronous job processing
4. **Database**: Generated asset metadata storage
5. **CDN**: Asset delivery optimization

## Conclusion

The ArtDept MCP Server provides a solid foundation for AI-powered creative asset generation using OpenAI's `gpt-image-1` model. Its base64-based architecture eliminates HTTP download dependencies, providing faster and more reliable image generation. The modular design, comprehensive error handling, extensive test coverage, and focus on professional quality output make it suitable for both development and production environments. The prompt engineering approach ensures consistent, high-quality results across all tool types while maintaining flexibility for diverse creative requirements.

Key advantages of the current implementation:
- **Reliability**: Direct base64 processing eliminates download failures
- **Speed**: No HTTP roundtrips for image retrieval
- **Testability**: Comprehensive mocked test suite with 15 test cases
- **Maintainability**: Clear separation of concerns and modular prompt builders
- **Professional Quality**: Tool-specific optimizations for different creative asset types
