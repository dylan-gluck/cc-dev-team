#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp>=1.0.0",
#     "openai>=1.0.0",
#     "pydantic>=2.0.0",
#     "pytest>=7.0.0",
#     "pytest-asyncio>=0.21.0",
# ]
# ///
"""
Comprehensive test script for ArtDept MCP Server.

This test suite validates all image generation functions with mocked OpenAI API calls,
verifies parameter handling, file operations, and error scenarios.

Usage:
    python test_server.py
    # or
    uv run test_server.py
"""

import asyncio
import base64
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch, mock_open

# Test data: Mock base64 encoded PNG (single pixel)
MOCK_B64_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

class TestArtDeptMCP(unittest.TestCase):
    """Test suite for ArtDept MCP Server functions."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_save_path = str(Path(self.test_dir) / "test_output")
        
        # Mock environment variable
        self.env_patcher = patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
        self.env_patcher.start()
        
        # Import main module after setting environment
        sys.path.insert(0, str(Path(__file__).parent))
        
        global main
        import main
        
        # Create mock OpenAI response
        self.mock_image_response = MagicMock()
        self.mock_image_response.b64_json = MOCK_B64_IMAGE
        
        self.mock_api_response = MagicMock()
        self.mock_api_response.data = [self.mock_image_response]

    def tearDown(self):
        """Clean up test environment."""
        self.env_patcher.stop()
        
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_generate_wireframe_desktop(self, mock_generate):
        """Test wireframe generation for desktop device."""
        mock_generate.return_value = self.mock_api_response
        
        result = await main.generate_wireframe(
            id="test-wireframe",
            prompt="Create a login form",
            device="desktop",
            style="minimalist",
            save=self.test_save_path
        )
        
        # Verify API call
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args
        self.assertEqual(call_args.kwargs['model'], "gpt-image-1")
        self.assertEqual(call_args.kwargs['size'], "1536x1024")
        self.assertEqual(call_args.kwargs['n'], 1)
        self.assertEqual(call_args.kwargs['quality'], "standard")
        self.assertEqual(call_args.kwargs['response_format'], "b64_json")
        
        # Verify result structure
        result_data = json.loads(result[0].text)
        self.assertTrue(result_data['success'])
        self.assertEqual(len(result_data['paths']), 1)
        self.assertTrue(result_data['paths'][0].endswith('test-wireframe-desktop.jpg'))

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_generate_wireframe_mobile(self, mock_generate):
        """Test wireframe generation for mobile device."""
        mock_generate.return_value = self.mock_api_response
        
        result = await main.generate_wireframe(
            id="test-mobile",
            prompt="Mobile app navigation",
            device="mobile",
            save=self.test_save_path
        )
        
        # Verify API call with mobile dimensions
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args
        self.assertEqual(call_args.kwargs['size'], "1024x1536")
        
        # Verify result
        result_data = json.loads(result[0].text)
        self.assertTrue(result_data['success'])
        self.assertTrue(result_data['paths'][0].endswith('test-mobile-mobile.jpg'))

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_generate_wireframe_both_devices(self, mock_generate):
        """Test wireframe generation for both devices."""
        mock_generate.return_value = self.mock_api_response
        
        result = await main.generate_wireframe(
            id="test-both",
            prompt="Responsive dashboard",
            device="both",
            save=self.test_save_path
        )
        
        # Should be called twice (desktop and mobile)
        self.assertEqual(mock_generate.call_count, 2)
        
        # Verify both sizes were called
        call_args_list = [call.kwargs['size'] for call in mock_generate.call_args_list]
        self.assertIn("1536x1024", call_args_list)  # desktop
        self.assertIn("1024x1536", call_args_list)  # mobile
        
        # Verify result has both files
        result_data = json.loads(result[0].text)
        self.assertTrue(result_data['success'])
        self.assertEqual(len(result_data['paths']), 2)

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_generate_design_system(self, mock_generate):
        """Test design system generation."""
        mock_generate.return_value = self.mock_api_response
        
        result = await main.generate_design_system(
            id="test-design",
            prompt="Corporate design system",
            n=3,
            type="brand",
            style="modern",
            colors="blue and white",
            save=self.test_save_path
        )
        
        # Should be called 3 times for 3 variations
        self.assertEqual(mock_generate.call_count, 3)
        
        # Verify API parameters
        for call in mock_generate.call_args_list:
            self.assertEqual(call.kwargs['model'], "gpt-image-1")
            self.assertEqual(call.kwargs['size'], "1536x1024")
            self.assertEqual(call.kwargs['n'], 1)
        
        # Verify result
        result_data = json.loads(result[0].text)
        self.assertTrue(result_data['success'])
        self.assertEqual(len(result_data['paths']), 3)
        
        # Check filenames
        expected_files = [f"test-design-v{i}.jpg" for i in range(1, 4)]
        for expected in expected_files:
            self.assertTrue(any(path.endswith(expected) for path in result_data['paths']))

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_generate_logo(self, mock_generate):
        """Test logo generation."""
        mock_generate.return_value = self.mock_api_response
        
        result = await main.generate_logo(
            id="test-logo",
            prompt="Tech startup logo",
            n=2,
            style="minimalist",
            colors="black",
            save=self.test_save_path
        )
        
        # Verify API calls
        self.assertEqual(mock_generate.call_count, 2)
        for call in mock_generate.call_args_list:
            self.assertEqual(call.kwargs['model'], "gpt-image-1")
            self.assertEqual(call.kwargs['size'], "1024x1024")
        
        # Verify PNG extension for logos
        result_data = json.loads(result[0].text)
        self.assertTrue(result_data['success'])
        self.assertEqual(len(result_data['paths']), 2)
        for path in result_data['paths']:
            self.assertTrue(path.endswith('.png'))

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_generate_icon(self, mock_generate):
        """Test icon generation."""
        mock_generate.return_value = self.mock_api_response
        
        result = await main.generate_icon(
            id="test-icon",
            prompt="Settings gear icon",
            n=1,
            style="flat",
            colors="blue",
            save=self.test_save_path
        )
        
        # Verify API call
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args
        self.assertEqual(call_args.kwargs['model'], "gpt-image-1")
        self.assertEqual(call_args.kwargs['size'], "1024x1024")
        
        # Verify PNG extension for icons
        result_data = json.loads(result[0].text)
        self.assertTrue(result_data['success'])
        self.assertTrue(result_data['paths'][0].endswith('.png'))

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_generate_illustration(self, mock_generate):
        """Test illustration generation with custom size."""
        mock_generate.return_value = self.mock_api_response
        
        result = await main.generate_illustration(
            id="test-illustration",
            prompt="Nature scene illustration",
            n=2,
            size="1536x1024",
            style="watercolor",
            save=self.test_save_path
        )
        
        # Verify API calls with custom size
        self.assertEqual(mock_generate.call_count, 2)
        for call in mock_generate.call_args_list:
            self.assertEqual(call.kwargs['model'], "gpt-image-1")
            self.assertEqual(call.kwargs['size'], "1536x1024")
        
        # Verify PNG extension for illustrations
        result_data = json.loads(result[0].text)
        self.assertTrue(result_data['success'])
        self.assertEqual(len(result_data['paths']), 2)
        for path in result_data['paths']:
            self.assertTrue(path.endswith('.png'))

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_generate_photo(self, mock_generate):
        """Test photo generation."""
        mock_generate.return_value = self.mock_api_response
        
        result = await main.generate_photo(
            id="test-photo",
            prompt="Portrait photography",
            n=1,
            size="1024x1536",
            style="professional",
            save=self.test_save_path
        )
        
        # Verify API call
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args
        self.assertEqual(call_args.kwargs['model'], "gpt-image-1")
        self.assertEqual(call_args.kwargs['size'], "1024x1536")
        
        # Verify JPG extension for photos
        result_data = json.loads(result[0].text)
        self.assertTrue(result_data['success'])
        self.assertTrue(result_data['paths'][0].endswith('.jpg'))

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_parameter_validation_n_constraint(self, mock_generate):
        """Test that n parameter is properly handled within constraints."""
        mock_generate.return_value = self.mock_api_response
        
        # Test with maximum allowed n=4
        result = await main.generate_logo(
            id="test-max-n",
            prompt="Logo test",
            n=4,
            save=self.test_save_path
        )
        
        self.assertEqual(mock_generate.call_count, 4)
        result_data = json.loads(result[0].text)
        self.assertTrue(result_data['success'])
        self.assertEqual(len(result_data['paths']), 4)

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_api_error_handling(self, mock_generate):
        """Test error handling when OpenAI API fails."""
        mock_generate.side_effect = Exception("API rate limit exceeded")
        
        result = await main.generate_logo(
            id="test-error",
            prompt="Logo test",
            n=1,
            save=self.test_save_path
        )
        
        result_data = json.loads(result[0].text)
        self.assertFalse(result_data['success'])
        # Check that we get an error message indicating failure
        self.assertTrue("0 logo(s)" in result_data['message'] or "failed" in result_data['message'].lower())
        self.assertEqual(len(result_data['paths']), 0)
        self.assertTrue(len(result_data['errors']) > 0)

    @patch('main.save_base64_image')
    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_file_save_error_handling(self, mock_generate, mock_save):
        """Test error handling when file saving fails."""
        mock_generate.return_value = self.mock_api_response
        mock_save.return_value = False  # Simulate save failure
        
        result = await main.generate_icon(
            id="test-save-error",
            prompt="Icon test",
            n=1,
            save=self.test_save_path
        )
        
        result_data = json.loads(result[0].text)
        self.assertFalse(result_data['success'])
        self.assertEqual(len(result_data['paths']), 0)
        self.assertTrue(len(result_data['errors']) > 0)

    async def test_save_base64_image_success(self):
        """Test successful base64 image saving."""
        import main
        
        test_file = Path(self.test_dir) / "test_image.png"
        success = await main.save_base64_image(MOCK_B64_IMAGE, test_file)
        
        self.assertTrue(success)
        self.assertTrue(test_file.exists())
        
        # Verify file content
        saved_data = test_file.read_bytes()
        expected_data = base64.b64decode(MOCK_B64_IMAGE)
        self.assertEqual(saved_data, expected_data)

    async def test_save_base64_image_directory_creation(self):
        """Test that parent directories are created when saving images."""
        import main
        
        nested_path = Path(self.test_dir) / "deep" / "nested" / "path" / "image.png"
        success = await main.save_base64_image(MOCK_B64_IMAGE, nested_path)
        
        self.assertTrue(success)
        self.assertTrue(nested_path.exists())
        self.assertTrue(nested_path.parent.exists())

    async def test_prompt_builders(self):
        """Test all prompt building functions."""
        import main
        
        # Test wireframe prompt
        wireframe_prompt = main.build_wireframe_prompt(
            "Login form", "desktop", "minimalist"
        )
        self.assertIn("Login form", wireframe_prompt)
        self.assertIn("desktop", wireframe_prompt)
        self.assertIn("minimalist", wireframe_prompt)
        
        # Test design system prompt
        design_prompt = main.build_design_system_prompt(
            "Brand system", "brand", "modern", "blue"
        )
        self.assertIn("Brand system", design_prompt)
        self.assertIn("brand", design_prompt)
        self.assertIn("blue", design_prompt)
        
        # Test logo prompt
        logo_prompt = main.build_logo_prompt("Tech logo", "minimal", "black")
        self.assertIn("Tech logo", logo_prompt)
        self.assertIn("minimal", logo_prompt)
        self.assertIn("black", logo_prompt)
        
        # Test icon prompt
        icon_prompt = main.build_icon_prompt("Settings icon", "flat", "blue")
        self.assertIn("Settings icon", icon_prompt)
        self.assertIn("flat", icon_prompt)
        self.assertIn("blue", icon_prompt)
        
        # Test illustration prompt
        illustration_prompt = main.build_illustration_prompt("Nature scene", "watercolor")
        self.assertIn("Nature scene", illustration_prompt)
        self.assertIn("watercolor", illustration_prompt)
        
        # Test photo prompt
        photo_prompt = main.build_photo_prompt("Portrait", "professional")
        self.assertIn("Portrait", photo_prompt)
        self.assertIn("professional", photo_prompt)

    @patch('main.client.images.generate', new_callable=AsyncMock)
    async def test_tool_call_routing(self, mock_generate):
        """Test that tool calls are routed correctly."""
        import main
        
        mock_generate.return_value = self.mock_api_response
        
        # Test each tool through the call_tool interface
        tools_to_test = [
            ("new_wireframe", {"id": "test", "prompt": "test wireframe"}),
            ("new_designsystem", {"id": "test", "prompt": "test design", "n": 1}),
            ("new_logo", {"id": "test", "prompt": "test logo", "n": 1}),
            ("new_icon", {"id": "test", "prompt": "test icon", "n": 1}),
            ("new_illustration", {"id": "test", "prompt": "test illustration", "n": 1}),
            ("new_photo", {"id": "test", "prompt": "test photo", "n": 1})
        ]
        
        for tool_name, args in tools_to_test:
            args["save"] = self.test_save_path
            result = await main.call_tool(tool_name, args)
            
            result_data = json.loads(result[0].text)
            self.assertTrue(result_data['success'], f"Tool {tool_name} failed")
        
        # Test unknown tool
        result = await main.call_tool("unknown_tool", {})
        result_data = json.loads(result[0].text)
        self.assertFalse(result_data['success'])
        self.assertIn("Unknown tool", result_data['message'])


async def run_tests():
    """Run all tests and display results."""
    print("ArtDept MCP Server - Comprehensive Test Suite")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestArtDeptMCP)
    
    # Custom test result to track pass/fail
    class TestResults:
        def __init__(self):
            self.tests_run = 0
            self.failures = []
            self.errors = []
            self.passes = 0
    
    results = TestResults()
    
    # Run each test manually to get async support
    test_methods = [
        'test_generate_wireframe_desktop',
        'test_generate_wireframe_mobile', 
        'test_generate_wireframe_both_devices',
        'test_generate_design_system',
        'test_generate_logo',
        'test_generate_icon',
        'test_generate_illustration',
        'test_generate_photo',
        'test_parameter_validation_n_constraint',
        'test_api_error_handling',
        'test_file_save_error_handling',
        'test_save_base64_image_success',
        'test_save_base64_image_directory_creation',
        'test_prompt_builders',
        'test_tool_call_routing'
    ]
    
    test_instance = TestArtDeptMCP()
    
    for method_name in test_methods:
        test_method = getattr(test_instance, method_name)
        results.tests_run += 1
        
        try:
            test_instance.setUp()
            if asyncio.iscoroutinefunction(test_method):
                await test_method()
            else:
                test_method()
            
            print(f"✓ {method_name}")
            results.passes += 1
            
        except Exception as e:
            print(f"✗ {method_name}: {str(e)}")
            results.failures.append((method_name, str(e)))
            
        finally:
            test_instance.tearDown()
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests run: {results.tests_run}")
    print(f"Passed: {results.passes}")
    print(f"Failed: {len(results.failures)}")
    print(f"Errors: {len(results.errors)}")
    
    if results.failures:
        print("\nFAILED TESTS:")
        for test_name, error in results.failures:
            print(f"  {test_name}: {error}")
    
    if results.passes == results.tests_run:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n❌ {len(results.failures)} TEST(S) FAILED")
        return 1


def main() -> int:
    """Main test execution function."""
    try:
        # Check environment
        if not os.getenv("OPENAI_API_KEY"):
            print("Warning: OPENAI_API_KEY not set. Using mock key for testing.")
            os.environ["OPENAI_API_KEY"] = "test-key-for-testing"
        
        # Run tests
        return asyncio.run(run_tests())
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 1
    except Exception as e:
        print(f"\nTest execution failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())