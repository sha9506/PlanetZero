"""
Chart Generation Service
Generates charts for user carbon emission data using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import List, Dict, Any
import base64
from io import BytesIO


class ChartService:
    """Service for generating carbon emission charts"""
    
    @staticmethod
    def generate_monthly_trend_chart(daily_emissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a line chart showing monthly emissions trend
        
        Args:
            daily_emissions: List of carbon footprint documents
            
        Returns:
            Chart data in JSON format for frontend
        """
        if not daily_emissions:
            return {
                "type": "line",
                "data": {
                    "labels": [],
                    "datasets": [{
                        "label": "Total Emissions",
                        "data": [],
                        "borderColor": "#10b981",
                        "backgroundColor": "rgba(16, 185, 129, 0.1)",
                        "tension": 0.4
                    }]
                },
                "isEmpty": True
            }
        
        # Sort by date
        sorted_emissions = sorted(daily_emissions, key=lambda x: x['date'])
        
        # Extract dates and total emissions
        dates = []
        totals = []
        
        for emission in sorted_emissions:
            date = emission['date']
            if isinstance(date, datetime):
                dates.append(date.strftime('%b %d'))
            else:
                dates.append(str(date))
            totals.append(round(emission.get('total_emissions', 0), 2))
        
        return {
            "type": "line",
            "data": {
                "labels": dates,
                "datasets": [{
                    "label": "Total Emissions (kg CO₂)",
                    "data": totals,
                    "borderColor": "#10b981",
                    "backgroundColor": "rgba(16, 185, 129, 0.1)",
                    "fill": True,
                    "tension": 0.4,
                    "pointRadius": 4,
                    "pointHoverRadius": 6
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "display": True,
                        "position": "top"
                    },
                    "tooltip": {
                        "mode": "index",
                        "intersect": False
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {
                            "display": True,
                            "text": "kg CO₂"
                        }
                    },
                    "x": {
                        "title": {
                            "display": True,
                            "text": "Date"
                        }
                    }
                }
            },
            "isEmpty": False
        }
    
    @staticmethod
    def generate_category_breakdown_chart(daily_emissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a pie/doughnut chart showing emissions by category
        
        Args:
            daily_emissions: List of carbon footprint documents
            
        Returns:
            Chart data in JSON format for frontend
        """
        if not daily_emissions:
            return {
                "type": "doughnut",
                "data": {
                    "labels": [],
                    "datasets": [{
                        "data": [],
                        "backgroundColor": []
                    }]
                },
                "isEmpty": True
            }
        
        # Aggregate emissions by category
        category_totals = {
            "Transport": 0,
            "Energy": 0,
            "Food": 0,
            "Water": 0,
            "Shopping": 0
        }
        
        for emission in daily_emissions:
            category_totals["Transport"] += emission.get('transport_emissions', 0)
            category_totals["Energy"] += emission.get('energy_emissions', 0)
            category_totals["Food"] += emission.get('food_emissions', 0)
            # Add water and shopping if they exist in the data
            if 'breakdown' in emission:
                breakdown = emission['breakdown']
                category_totals["Water"] += breakdown.get('water', 0)
                category_totals["Shopping"] += breakdown.get('shopping', 0)
        
        # Filter out zero values and round
        labels = []
        data = []
        colors = {
            "Transport": "#ef4444",
            "Energy": "#f59e0b",
            "Food": "#10b981",
            "Water": "#3b82f6",
            "Shopping": "#8b5cf6"
        }
        background_colors = []
        
        for category, value in category_totals.items():
            if value > 0:
                labels.append(category)
                data.append(round(value, 2))
                background_colors.append(colors[category])
        
        return {
            "type": "doughnut",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Emissions by Category",
                    "data": data,
                    "backgroundColor": background_colors,
                    "borderColor": "#ffffff",
                    "borderWidth": 2,
                    "hoverOffset": 4
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "display": True,
                        "position": "right"
                    }
                }
            },
            "isEmpty": False
        }
    
    @staticmethod
    def generate_weekly_comparison_chart(daily_emissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a bar chart comparing emissions across days of the week
        
        Args:
            daily_emissions: List of carbon footprint documents
            
        Returns:
            Chart data in JSON format for frontend
        """
        if not daily_emissions:
            return {
                "type": "bar",
                "data": {
                    "labels": [],
                    "datasets": []
                },
                "isEmpty": True
            }
        
        # Group by day of week
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_totals = {day: [] for day in days}
        
        for emission in daily_emissions:
            date = emission['date']
            if isinstance(date, datetime):
                day_name = days[date.weekday()]
                day_totals[day_name].append(emission.get('total_emissions', 0))
        
        # Calculate averages
        labels = []
        data = []
        
        for day in days:
            if day_totals[day]:
                labels.append(day)
                avg = sum(day_totals[day]) / len(day_totals[day])
                data.append(round(avg, 2))
        
        return {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Average Daily Emissions",
                    "data": data,
                    "backgroundColor": "rgba(16, 185, 129, 0.6)",
                    "borderColor": "#10b981",
                    "borderWidth": 2
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "display": True,
                        "position": "top"
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {
                            "display": True,
                            "text": "kg CO₂"
                        }
                    }
                }
            },
            "isEmpty": False
        }
    
    @staticmethod
    def generate_all_charts(daily_emissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate all charts for the dashboard
        
        Args:
            daily_emissions: List of carbon footprint documents
            
        Returns:
            Dictionary containing all chart data
        """
        return {
            "monthly_trend": ChartService.generate_monthly_trend_chart(daily_emissions),
            "category_breakdown": ChartService.generate_category_breakdown_chart(daily_emissions),
            "weekly_comparison": ChartService.generate_weekly_comparison_chart(daily_emissions)
        }
