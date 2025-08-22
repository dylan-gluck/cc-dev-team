# SudoLang Syntax Cheatsheet

## Basic Structure

### Markdown Preamble
```sudo
# Program Title
Description of the program, AI roles, and expertise to leverage.
```

### Interfaces
```sudo
interface InterfaceName {
  property = value
  functionName(arg1, arg2)
}

// Short form (interface keyword optional)
InterfaceName {
  property = value
}
```

## Variables & Assignments

```sudo
// Basic assignment
variable = value

// Operations and assignment
counter += 1  // Increment
total -= n    // Decrement
price *= n    // Multiply and assign
share /= n    // Divide and assign

// Template strings
greeting = "Hello, $name"
escaped = "This will not \\$interpolate"
```

## Control Flow

### Conditionals
```sudo
// If-else
if (condition) {
  // code
} else {
  // code
}

// Ternary-style assignment
status = if (age >= 18) "adult" else "minor"
```

### Loops
```sudo
// Natural forEach
for each item, doSomething(item)

// While loop
while (condition) {
  // code
}

// Infinite loop
loop {
  // code
}
```

## Functions

```sudo
// Inferred function (no body needed)
fn functionName
function functionName

// Function with parameters (no body)
function greet(name)

// Function with body
fn calculateTotal(price, quantity) {
  return price * quantity
}

// Arrow function
add = (a, b) => a + b

// Function call
result = functionName(arg1, arg2)
```

## Function Composition

```sudo
// Pipe operator
processData = parse |> validate |> transform

// Usage
processData(input)  // Equivalent to transform(validate(parse(input)))
```

## Commands

```sudo
// Command definition
/commandName [parameter] - Description of what this command does

// Command with shortcut
/c | commandName [parameter] - Description with shortcut

// Example in interface
Bot {
  /h | help - Display help information
  /q | quit - Exit the program
}
```

## Constraints & Requirements

```sudo
// Constraint (natural language)
constraint {
  Always respond in a friendly manner.
  Keep responses under 100 words.
}

// Named constraint
constraint ResponseStyle {
  Use simple, concise language.
  Avoid technical jargon.
}

// Requirement (throws error when violated)
require {
  Input must be a valid email address.
  throw "Invalid email format"
}

// Warning (doesn't throw error)
warn {
  Password should contain special characters.
}
```

## Operators

### Logical Operators
```sudo
a && b    // AND
a || b    // OR
a xor b   // XOR
!a        // NOT
```

### Math Operators
```sudo
a + b     // Addition
a - b     // Subtraction
a * b     // Multiplication
a / b     // Division
a ^ b     // Exponent
a % b     // Remainder
a union b      // Union
a intersection b  // Intersection
```

### Range Operator
```sudo
1..5      // Range: 1,2,3,4,5
```

## Pattern Matching

```sudo
// Basic pattern matching
result = match (value) {
  case pattern1 => result1
  case pattern2 => result2
  default => defaultResult
}

// With destructuring
result = match (shape) {
  case {type: "circle", radius} => "Circle with radius: $radius"
  case {type: "rectangle", width, height} => "Rectangle: ${width}x${height}"
  default => "Unknown shape"
}

// Semantic pattern matching
(user question contains "help") => showHelp()
```

## Destructuring

```sudo
// Array destructuring
[first, second] = [1, 2]

// Object destructuring
{name, age} = {name: "Alice", age: 30}
```

## Modifiers

```sudo
// Function with modifiers
explain(topic):length=short, detail=simple

// Command with modifiers
/search [query]:sort=relevance, limit=10
```

## Mermaid Diagrams

```sudo
```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
```

## Options

```sudo
Options {
  depth: 1..10
  mode: "simple" | "advanced"
}

// Usage in commands
/query [text] -depth 5 -mode advanced
```

## SudoLang Style Best Practices

1. Favor natural language over code when possible
2. Use inference for function bodies when appropriate
3. Keep code minimal and focused on structure
4. Use constraints for declarative behavior definition
5. Prefer composition over inheritance
6. Use interfaces instead of classes
7. Express requirements and constraints clearly
8. Use markdown for organization and documentation
