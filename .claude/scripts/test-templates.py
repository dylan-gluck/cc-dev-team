#!/usr/bin/env python3
"""Test template system functionality."""

import json
import os
from pathlib import Path
from typing import Dict, List

def load_template(template_path: Path) -> Dict:
    """Load and parse a template JSON file."""
    with open(template_path, 'r') as f:
        return json.load(f)

def validate_template(template: Dict, path: Path) -> List[str]:
    """Validate template structure and return any errors."""
    errors = []
    required_fields = ['name', 'displayName', 'description', 'category', 'stack', 'structure']
    
    for field in required_fields:
        if field not in template:
            errors.append(f"Missing required field: {field}")
    
    # Validate structure
    if 'structure' in template:
        if 'root' not in template['structure']:
            errors.append("Missing 'root' in structure")
        if 'directories' not in template['structure']:
            errors.append("Missing 'directories' in structure")
        elif not isinstance(template['structure']['directories'], list):
            errors.append("'directories' must be a list")
    
    # Validate stack
    if 'stack' in template:
        if 'primary' not in template['stack']:
            errors.append("Missing 'primary' in stack")
    
    # Validate category matches directory
    if 'category' in template:
        actual_category = path.parent.name
        if template['category'] != actual_category:
            errors.append(f"Category mismatch: template says '{template['category']}' but in '{actual_category}' directory")
    
    return errors

def test_templates():
    """Test all templates in the system."""
    templates_dir = Path('.claude/templates')
    
    if not templates_dir.exists():
        print("❌ Templates directory not found!")
        return False
    
    all_valid = True
    template_count = 0
    templates_by_category = {}
    
    print("Template System Test Report")
    print("=" * 50)
    print()
    
    # Find all template JSON files
    for template_path in templates_dir.glob('**/*.json'):
        template_count += 1
        category = template_path.parent.name
        
        if category not in templates_by_category:
            templates_by_category[category] = []
        
        try:
            # Load template
            template = load_template(template_path)
            templates_by_category[category].append(template['name'])
            
            # Validate template
            errors = validate_template(template, template_path)
            
            if errors:
                all_valid = False
                print(f"❌ {template_path.relative_to(templates_dir)}")
                for error in errors:
                    print(f"   - {error}")
            else:
                print(f"✅ {template_path.relative_to(templates_dir)}: {template['displayName']}")
                
        except json.JSONDecodeError as e:
            all_valid = False
            print(f"❌ {template_path.relative_to(templates_dir)}: Invalid JSON - {e}")
        except Exception as e:
            all_valid = False
            print(f"❌ {template_path.relative_to(templates_dir)}: Error - {e}")
    
    print()
    print("Summary")
    print("-" * 50)
    print(f"Total templates: {template_count}")
    print(f"Categories: {len(templates_by_category)}")
    
    for category, templates in sorted(templates_by_category.items()):
        print(f"  {category}: {', '.join(templates)}")
    
    print()
    if all_valid:
        print("✅ All templates are valid!")
    else:
        print("❌ Some templates have errors. Please fix them.")
    
    return all_valid

def list_available_templates():
    """List all available templates for user selection."""
    templates_dir = Path('.claude/templates')
    templates = []
    
    for template_path in templates_dir.glob('**/*.json'):
        try:
            template = load_template(template_path)
            templates.append({
                'name': template['name'],
                'displayName': template['displayName'],
                'description': template['description'],
                'category': template['category'],
                'path': str(template_path)
            })
        except:
            pass
    
    if templates:
        print("\nAvailable Templates:")
        print("-" * 50)
        for i, t in enumerate(templates, 1):
            print(f"{i}. {t['displayName']} ({t['name']})")
            print(f"   {t['description']}")
            print(f"   Category: {t['category']}")
            print()
    
    return templates

if __name__ == "__main__":
    # Test all templates
    success = test_templates()
    
    # List available templates
    templates = list_available_templates()
    
    # Exit with appropriate code
    exit(0 if success else 1)