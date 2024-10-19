import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
import matplotlib.pyplot as plt
import ezdxf

class FoundationEstimator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Foundation Quantity Estimator')
        
        # Layout and input fields
        self.layout = QVBoxLayout()
        
        self.length_label = QLabel('Length of Foundation Pad (m):')
        self.length_input = QLineEdit(self)
        
        self.width_label = QLabel('Width of Foundation Pad (m):')
        self.width_input = QLineEdit(self)
        
        self.depth_excavation_label = QLabel('Depth of Excavation (m):')
        self.depth_excavation_input = QLineEdit(self)
        
        self.soling_thickness_label = QLabel('Thickness of Soling (m):')
        self.soling_thickness_input = QLineEdit(self)
        
        self.pcc_thickness_label = QLabel('Thickness of PCC (m):')
        self.pcc_thickness_input = QLineEdit(self)
        
        self.rcc_thickness_label = QLabel('Thickness of RCC (m):')
        self.rcc_thickness_input = QLineEdit(self)
        
        self.trap_height_label = QLabel('Height of Trapezoidal Section (m):')
        self.trap_height_input = QLineEdit(self)
        
        self.column_height_label = QLabel('Height of Column (m):')
        self.column_height_input = QLineEdit(self)
        
        self.column_width_label = QLabel('Width of Column Section (m):')
        self.column_width_input = QLineEdit(self)
        
        self.column_length_label = QLabel('Length of Column Section (m):')
        self.column_length_input = QLineEdit(self)
        
        self.calculate_btn = QPushButton('Calculate Quantities', self)
        self.calculate_btn.clicked.connect(self.calculate_quantities)
        
        # Buttons for exporting
        self.export_excel_btn = QPushButton('Export to Excel', self)
        self.export_excel_btn.clicked.connect(self.export_to_excel)
        
        self.export_cad_btn = QPushButton('Export to CAD (DXF)', self)
        self.export_cad_btn.clicked.connect(self.export_to_cad)
        
        # Adding all input fields to the layout
        self.layout.addWidget(self.length_label)
        self.layout.addWidget(self.length_input)
        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_input)
        self.layout.addWidget(self.depth_excavation_label)
        self.layout.addWidget(self.depth_excavation_input)
        self.layout.addWidget(self.soling_thickness_label)
        self.layout.addWidget(self.soling_thickness_input)
        self.layout.addWidget(self.pcc_thickness_label)
        self.layout.addWidget(self.pcc_thickness_input)
        self.layout.addWidget(self.rcc_thickness_label)
        self.layout.addWidget(self.rcc_thickness_input)
        self.layout.addWidget(self.trap_height_label)
        self.layout.addWidget(self.trap_height_input)
        self.layout.addWidget(self.column_height_label)
        self.layout.addWidget(self.column_height_input)
        self.layout.addWidget(self.column_width_label)
        self.layout.addWidget(self.column_width_input)
        self.layout.addWidget(self.column_length_label)
        self.layout.addWidget(self.column_length_input)
        self.layout.addWidget(self.calculate_btn)
        self.layout.addWidget(self.export_excel_btn)
        self.layout.addWidget(self.export_cad_btn)
        
        self.result_label = QLabel('Results will be shown here.')
        self.layout.addWidget(self.result_label)
        
        # Set layout
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def calculate_quantities(self):
        # Get input values
        length = float(self.length_input.text())
        width = float(self.width_input.text())
        depth_excavation = float(self.depth_excavation_input.text())
        soling_thickness = float(self.soling_thickness_input.text())
        pcc_thickness = float(self.pcc_thickness_input.text())
        rcc_thickness = float(self.rcc_thickness_input.text())
        trap_height = float(self.trap_height_input.text())
        column_height = float(self.column_height_input.text())
        column_width = float(self.column_width_input.text())
        column_length = float(self.column_length_input.text())
        
        # Calculations for volumes
        excavation_volume = self.calculate_volume(length, width, depth_excavation)
        soling_volume = self.calculate_volume(length, width, soling_thickness)
        pcc_volume = self.calculate_volume(length, width, pcc_thickness)
        rcc_volume = self.calculate_volume(length, width, rcc_thickness)
        trap_volume = self.calculate_trapezoidal_volume(length, width, trap_height)
        column_volume = self.calculate_volume(column_length, column_width, column_height)
        
        # Display the results
        self.result_label.setText(f"Excavation: {excavation_volume:.2f} m³\nSoling: {soling_volume:.2f} m³\nPCC: {pcc_volume:.2f} m³\nRCC: {rcc_volume:.2f} m³\nTrapezoidal: {trap_volume:.2f} m³\nColumn: {column_volume:.2f} m³")
        
        # Save the calculated values for exporting
        self.calculated_quantities = {
            'excavation_volume': excavation_volume,
            'soling_volume': soling_volume,
            'pcc_volume': pcc_volume,
            'rcc_volume': rcc_volume,
            'trap_volume': trap_volume,
            'column_volume': column_volume
        }
        
        # Show drawing (plan and elevation)
        self.draw_foundation_views(length, width, depth_excavation, soling_thickness, pcc_thickness, rcc_thickness, trap_height, column_height, column_width, column_length)
    
    def calculate_volume(self, length, width, height):
        return length * width * height

    def calculate_trapezoidal_volume(self, length, width, height):
        top_length = length - 0.1  # Reduced top width (example)
        top_width = width - 0.1
        return height * (length * width + top_length * top_width) / 2

    def draw_foundation_views(self, length, width, depth_excavation, soling_thickness, pcc_thickness, rcc_thickness, trap_height, column_height, column_width, column_length):
        fig, (ax_plan, ax_elevation) = plt.subplots(2, 1, figsize=(8, 12))

        ### Plan View (Top View) ###
        ax_plan.set_title("Foundation Plan View")
        
        # Drawing the outer boundary of the foundation (Footing)
        ax_plan.plot([0, length], [0, 0], 'k-')  # Bottom
        ax_plan.plot([length, length], [0, width], 'k-')  # Right
        ax_plan.plot([length, 0], [width, width], 'k-')  # Top
        ax_plan.plot([0, 0], [width, 0], 'k-')  # Left
        
        # Drawing the internal column section in the foundation
        column_start_x = (length - column_length) / 2
        column_end_x = column_start_x + column_length
        column_start_y = (width - column_width) / 2
        column_end_y = column_start_y + column_width
        
        ax_plan.plot([column_start_x, column_end_x], [column_start_y, column_start_y], 'r-')  # Top of the column
        ax_plan.plot([column_end_x, column_end_x], [column_start_y, column_end_y], 'r-')  # Right side of the column
        ax_plan.plot([column_end_x, column_start_x], [column_end_y, column_end_y], 'r-')  # Bottom of the column
        ax_plan.plot([column_start_x, column_start_x], [column_end_y, column_start_y], 'r-')  # Left side of the column
        
        # Annotations
        ax_plan.text(length / 2, -0.05, f'Length: {length}m', ha='center')
        ax_plan.text(-0.1, width / 2, f'Width: {width}m', va='center', rotation='vertical')
        ax_plan.text((column_start_x + column_end_x) / 2, column_start_y - 0.05, f'Column', ha='center', color='red')

        ax_plan.set_xlim([-0.5, length + 0.5])
        ax_plan.set_ylim([-0.5, width + 0.5])
        ax_plan.set_aspect('equal')
        ax_plan.set_xlabel("Length (m)")
        ax_plan.set_ylabel("Width (m)")
        
        ### Elevation View (Side View) ###
        ax_elevation.set_title("Foundation Elevation View")

        # 1. Excavation
        ax_elevation.plot([0, length], [0, 0], 'k-', label="Excavation")
        ax_elevation.plot([length, length], [0, -depth_excavation], 'k-')
        ax_elevation.plot([length, 0], [-depth_excavation, -depth_excavation], 'k-')
        ax_elevation.plot([0, 0], [-depth_excavation, 0], 'k-')
        
        # Annotations
        ax_elevation.text(length / 2, -depth_excavation - 0.2, 'Excavation', ha='center', color='k')

        # 2. Soling
        soling_top = -depth_excavation + soling_thickness
        ax_elevation.plot([0, length], [-depth_excavation, -depth_excavation], 'b-', label="Soling")
        ax_elevation.plot([length, length], [-depth_excavation, soling_top], 'b-')
        ax_elevation.plot([length, 0], [soling_top, soling_top], 'b-')
        ax_elevation.plot([0, 0], [soling_top, -depth_excavation], 'b-')
        
        # 3. PCC (Plain Cement Concrete)
        pcc_top = soling_top + pcc_thickness
        ax_elevation.plot([0, length], [soling_top, soling_top], 'g-', label="PCC")
        ax_elevation.plot([length, length], [soling_top, pcc_top], 'g-')
        ax_elevation.plot([length, 0], [pcc_top, pcc_top], 'g-')
        ax_elevation.plot([0, 0], [pcc_top, soling_top], 'g-')

        # 4. RCC (Reinforced Cement Concrete - Rectangular Part)
        rcc_top = pcc_top + rcc_thickness
        ax_elevation.plot([0, length], [pcc_top, pcc_top], 'r-', label="RCC")
        ax_elevation.plot([length, length], [pcc_top, rcc_top], 'r-')
        ax_elevation.plot([length, 0], [rcc_top, rcc_top], 'r-')
        ax_elevation.plot([0, 0], [rcc_top, pcc_top], 'r-')

        # 5. Trapezoidal Part
        trap_top = rcc_top + trap_height
        ax_elevation.plot([0, length], [rcc_top, rcc_top], 'm-', label="Trapezoidal")
        ax_elevation.plot([length, length - 0.1], [rcc_top, trap_top], 'm-')
        ax_elevation.plot([length - 0.1, 0.1], [trap_top, trap_top], 'm-')
        ax_elevation.plot([0.1, 0], [trap_top, rcc_top], 'm-')

        # 6. Column (Starting above the Trapezoidal Part)
        column_top = trap_top + column_height
        ax_elevation.plot([0.1, length - 0.1], [trap_top, trap_top], 'c-', label="Column")
        ax_elevation.plot([length - 0.1, length - 0.1], [trap_top, column_top], 'c-')
        ax_elevation.plot([length - 0.1, 0.1], [column_top, column_top], 'c-')
        ax_elevation.plot([0.1, 0.1], [column_top, trap_top], 'c-')

        # Labels for the Elevation View
        ax_elevation.set_xlim([-0.5, length + 0.5])
        ax_elevation.set_ylim([-depth_excavation - 1, column_top + 1])
        ax_elevation.set_xlabel("Length (m)")
        ax_elevation.set_ylabel("Height (m)")

        # Show both views
        plt.tight_layout()
        plt.show()

    def export_to_excel(self):
        # Open a file dialog to choose the save location for the Excel file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)", options=options)
        if file_path:
            self.generate_excel_output(file_path)

    def generate_excel_output(self, file_path):
        # Data to be written to the Excel sheet
        data = [
            [1, 'Excavation', 'm³', 1, float(self.length_input.text()), float(self.width_input.text()), float(self.depth_excavation_input.text()), self.calculated_quantities['excavation_volume'], 'Depth as per design'],
            [2, 'Soling (Stone)', 'm³', 1, float(self.length_input.text()), float(self.width_input.text()), float(self.soling_thickness_input.text()), self.calculated_quantities['soling_volume'], 'Stone soling thickness'],
            [3, 'PCC (Plain Cement Concrete)', 'm³', 1, float(self.length_input.text()), float(self.width_input.text()), float(self.pcc_thickness_input.text()), self.calculated_quantities['pcc_volume'], 'Thickness of PCC layer'],
            [4, 'RCC (Reinforced Cement Concrete)', 'm³', 1, float(self.length_input.text()), float(self.width_input.text()), float(self.rcc_thickness_input.text()), self.calculated_quantities['rcc_volume'], 'Reinforced section'],
            [5, 'Trapezoidal Section', 'm³', 1, float(self.length_input.text()), float(self.width_input.text()), float(self.trap_height_input.text()), self.calculated_quantities['trap_volume'], 'For load distribution'],
            [6, 'Column', 'm³', 1, float(self.column_length_input.text()), float(self.column_width_input.text()), float(self.column_height_input.text()), self.calculated_quantities['column_volume'], 'Column height and size']
        ]
        
        # Creating a DataFrame
        df = pd.DataFrame(data, columns=['S.N', 'Description of Item', 'Unit', 'Number', 'Length (m)', 'Width (m)', 'Height (m)', 'Quantity', 'Remarks'])
        
        # Saving to Excel
        df.to_excel(file_path, index=False)
        print(f"Excel file saved as {file_path}")

    def export_to_cad(self):
        # Open a file dialog to choose the save location for the CAD file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CAD File", "", "CAD Files (*.dxf)", options=options)
        if file_path:
            self.generate_cad_drawing(file_path)

    def generate_cad_drawing(self, file_path):
        doc = ezdxf.new()
        msp = doc.modelspace()
        
        # Draw foundation lines
        length = float(self.length_input.text())
        width = float(self.width_input.text())
        column_length = float(self.column_length_input.text())
        column_width = float(self.column_width_input.text())
        total_height = float(self.depth_excavation_input.text()) + float(self.soling_thickness_input.text()) + \
                       float(self.pcc_thickness_input.text()) + float(self.rcc_thickness_input.text()) + \
                       float(self.trap_height_input.text()) + float(self.column_height_input.text())
        
        msp.add_line((0, 0), (length, 0))  # Bottom line
        msp.add_line((length, 0), (length, total_height))  # Right line
        msp.add_line((length, total_height), (0, total_height))  # Top line
        msp.add_line((0, total_height), (0, 0))  # Left line
        
        # Draw the column
        column_bottom_y = total_height - float(self.column_height_input.text())
        msp.add_line((column_length / 2, column_bottom_y), (column_length / 2 + column_length, column_bottom_y))  # Bottom line of the column
        msp.add_line((column_length / 2 + column_length, column_bottom_y), (column_length / 2 + column_length, total_height))  # Right line of the column
        msp.add_line((column_length / 2 + column_length, total_height), (column_length / 2, total_height))  # Top line of the column
        msp.add_line((column_length / 2, total_height), (column_length / 2, column_bottom_y))  # Left line of the column
        
        # Save the CAD file
        doc.saveas(file_path)
        print(f"CAD drawing saved as {file_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FoundationEstimator()
    ex.show()
    sys.exit(app.exec_())
