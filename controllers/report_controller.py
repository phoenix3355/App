"""
Report Controller
Business logic for generating reports using Jinja2 templates.
"""
from typing import List, Optional
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from models import get_db
from models.instrument import Instrument
from models.calibration import Calibration
from models.inventory import Inventory

class ReportController:
    """Controller for report generation operations."""
    
    def __init__(self):
        # Setup Jinja2 environment
        template_dir = Path(__file__).resolve().parent.parent / 'reports' / 'templates'
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def generate_instrument_report(self, instrument_ids: Optional[List[int]] = None) -> str:
        """
        Generate HTML report for instruments.
        
        Args:
            instrument_ids: Optional list of instrument IDs to include
            
        Returns:
            HTML report string
        """
        db = get_db()
        try:
            query = db.query(Instrument)
            if instrument_ids:
                query = query.filter(Instrument.id.in_(instrument_ids))
            
            instruments = query.all()
            
            template = self.env.get_template('instrument_report.html')
            html = template.render(
                instruments=instruments,
                report_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                title='Instrument Report'
            )
            
            return html
        finally:
            db.close()
    
    def generate_calibration_report(self, instrument_id: Optional[int] = None,
                                   start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None) -> str:
        """
        Generate HTML report for calibrations.
        
        Args:
            instrument_id: Optional instrument ID to filter
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            HTML report string
        """
        db = get_db()
        try:
            query = db.query(Calibration)
            
            if instrument_id:
                query = query.filter(Calibration.instrument_id == instrument_id)
            if start_date:
                query = query.filter(Calibration.calibration_date >= start_date)
            if end_date:
                query = query.filter(Calibration.calibration_date <= end_date)
            
            calibrations = query.order_by(Calibration.calibration_date.desc()).all()
            
            template = self.env.get_template('calibration_report.html')
            html = template.render(
                calibrations=calibrations,
                report_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                title='Calibration Report',
                start_date=start_date.strftime('%Y-%m-%d') if start_date else 'All',
                end_date=end_date.strftime('%Y-%m-%d') if end_date else 'All'
            )
            
            return html
        finally:
            db.close()
    
    def generate_inventory_report(self) -> str:
        """
        Generate HTML report for inventory.
        
        Returns:
            HTML report string
        """
        db = get_db()
        try:
            inventory_items = db.query(Inventory).all()
            
            template = self.env.get_template('inventory_report.html')
            html = template.render(
                inventory_items=inventory_items,
                report_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                title='Inventory Report'
            )
            
            return html
        finally:
            db.close()
    
    def save_report(self, html_content: str, filename: str) -> str:
        """
        Save HTML report to file.
        
        Args:
            html_content: HTML content to save
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        output_dir = Path(__file__).resolve().parent.parent / 'reports' / 'output'
        output_dir.mkdir(exist_ok=True)
        
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)

# Create singleton instance
report_controller = ReportController()
