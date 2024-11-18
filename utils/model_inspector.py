# utils/model_inspector.py

from django.apps import apps
from django.db import models
from django.db.models.fields.related import (
    ForeignKey, OneToOneField, ManyToManyField
)
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import json
from collections import defaultdict

class ModelRelationshipInspector:
    """Utility class to inspect Django model relationships."""
    
    def __init__(self, app_label=None):
        """
        Initialize the inspector.
        
        Args:
            app_label: Optional app label to limit inspection to a specific app.
        """
        self.app_label = app_label
    
    def get_all_models(self):
        """Get all models or models from a specific app."""
        if self.app_label:
            return apps.get_app_config(self.app_label).get_models()
        return apps.get_models()
    
    def get_field_relationship_type(self, field):
        """Determine the type of relationship field."""
        if isinstance(field, ForeignKey):
            return 'ForeignKey'
        elif isinstance(field, OneToOneField):
            return 'OneToOneField'
        elif isinstance(field, ManyToManyField):
            return 'ManyToManyField'
        elif isinstance(field, GenericForeignKey):
            return 'GenericForeignKey'
        elif isinstance(field, GenericRelation):
            return 'GenericRelation'
        return None
    
    def get_model_relationships(self):
        """Get all relationships between models."""
        relationships = defaultdict(list)
        
        for model in self.get_all_models():
            model_name = f"{model._meta.app_label}.{model._meta.model_name}"
            
            # Get all fields including reverse relations
            for field in model._meta.get_fields():
                rel_type = self.get_field_relationship_type(field)
                if rel_type:
                    related_model = (
                        field.related_model._meta.label
                        if hasattr(field, 'related_model') and field.related_model
                        else 'Generic'
                    )
                    field_name = field.name
                    
                    relationships[model_name].append({
                        'field_name': field_name,
                        'relationship_type': rel_type,
                        'related_model': related_model,
                        'related_name': getattr(field, 'related_name', None)
                    })
        
        return relationships
    
    def generate_mermaid_diagram(self):
        """Generate a Mermaid diagram of model relationships."""
        relationships = self.get_model_relationships()
        
        mermaid_code = ["classDiagram"]
        
        # Add relationships
        for model, relations in relationships.items():
            for relation in relations:
                rel_type = relation['relationship_type']
                related_model = relation['related_model']
                
                if rel_type == 'ForeignKey':
                    arrow = "-->"
                elif rel_type == 'OneToOneField':
                    arrow = "--o"
                elif rel_type == 'ManyToManyField':
                    arrow = "--*"
                else:
                    continue
                
                line = f"    {model.split('.')[-1]} {arrow} {related_model.split('.')[-1]} : {relation['field_name']}"
                mermaid_code.append(line)
        
        return "\n".join(mermaid_code)
    
    def print_relationships(self):
        """Print relationships in a readable format."""
        relationships = self.get_model_relationships()
        
        for model, relations in relationships.items():
            print(f"\nModel: {model}")
            for relation in relations:
                print(f"  ├─ {relation['field_name']} ({relation['relationship_type']})")
                print(f"  │  └─ Related to: {relation['related_model']}")
                if relation['related_name']:
                    print(f"  │     └─ Related name: {relation['related_name']}")

def inspect_models(app_label=None):
    """Utility function to get JSON representation of model relationships."""
    inspector = ModelRelationshipInspector(app_label)
    return json.dumps(inspector.get_model_relationships(), indent=2)

def generate_relationship_diagram(app_label=None):
    """Generate a Mermaid diagram for model relationships."""
    inspector = ModelRelationshipInspector(app_label)
    return inspector.generate_mermaid_diagram()
