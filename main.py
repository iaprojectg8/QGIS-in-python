from utils.imports import *
from algorithms.Script_Préparation_Données import ExtractionDuFichierCsvPourOutilIa

def make_csv(city):
    return city+".csv"

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Parameters")
        self.setMinimumWidth(800)

        # Initialize autocomplete flag
        self.autocomplete_enabled = False

        # Create layout
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Create input fields
        self.image_landsat_9 = self.create_file_input()
        self.numro_de_bande_de_la_lst = QSpinBox()
        self.numro_de_bande_de_la_lst.setMinimum(1)
        self.numro_de_bande_de_la_lst.setValue(7)

        self.rsolution_de_la_couche_lst_m = QDoubleSpinBox()
        self.rsolution_de_la_couche_lst_m.setMinimum(0)
        self.rsolution_de_la_couche_lst_m.setValue(30)

        self.raster_du_mnt = self.create_file_input()
        self.raster_de_loccupation_du_sol_dwv1 = self.create_file_input()
        self.raster_de_la_nature_du_sol = self.create_file_input()
        self.raster_de_la_hauteur_arbore = self.create_file_input()
        self.raster_de_la_catgorie_hydrologique = self.create_file_input()
        self.raster_de_la_zone_climatique_lcz = self.create_file_input()
        self.emprise_de_calcul_de_luhi = QLineEdit()
        self.nom_du_champ_daltitude = QLineEdit("ALT")
        self.nom_du_champ_de_nature_du_sol = QLineEdit("NATSOL")
        self.nom_du_champ_de_pente = QLineEdit("PENTE")
        self.nom_du_champ_dexposition = QLineEdit("EXP")
        self.nom_du_champ_doccupation_du_sol = QLineEdit("OCCSOL")
        self.nom_du_champ_pour_le_caractre_urbainrural = QLineEdit("URB")
        self.nom_du_champ_de_hauteur_arbore = QLineEdit("HAUTA")
        self.nom_du_champ_de_catgorie_hydrologique = QLineEdit("CATHYD")
        self.nom_du_champ_de_zone_climatique = QLineEdit("ZONECL")
        self.nom_du_champ_dalbedo = QLineEdit("ALB")
        self.tableur_sortie = self.create_file_output()

        # Add input fields to form layout
        form_layout.addRow("Image LandSat 9", self.image_landsat_9)
        form_layout.addRow("Numéro de bande de la LST", self.numro_de_bande_de_la_lst)
        form_layout.addRow("Résolution de la couche LST (m)", self.rsolution_de_la_couche_lst_m)
        form_layout.addRow("Raster du MNT", self.raster_du_mnt)
        form_layout.addRow("Raster de l'occupation du sol (DWV1)", self.raster_de_loccupation_du_sol_dwv1)
        form_layout.addRow("Raster de la nature du sol", self.raster_de_la_nature_du_sol)
        form_layout.addRow("Raster de la hauteur arborée", self.raster_de_la_hauteur_arbore)
        form_layout.addRow("Raster de la catégorie hydrologique", self.raster_de_la_catgorie_hydrologique)
        form_layout.addRow("Raster de la zone climatique (LCZ)", self.raster_de_la_zone_climatique_lcz)

        # Add EPSG selection widget
        self.epsg_widget = QgsProjectionSelectionWidget()
        self.epsg_widget.setCrs(QgsCoordinateReferenceSystem())  # Set default EPSG here
        form_layout.addRow("Sélectionner EPSG", self.epsg_widget)

        form_layout.addRow("Tableur en sortie",self.tableur_sortie)

        epsg_text = self.epsg_widget.crs().authid()
        epsg_num = epsg_text.split(":")[-1]

        self.label_to_filename = { # les noms seront à changer mais au moins je sais que c'est ici que je vais pouvoir les définir
            "Image LandSat 9" : f"LST_{epsg_num}.tif",
            "Raster du MNT": f"DEM_{epsg_num}.tif",
            "Raster de l'occupation du sol (DWV1)": f"Land_Cover_{epsg_num}.tif",
            "Raster de la nature du sol": f"Soil_Texture_{epsg_num}.tif",
            "Raster de la hauteur arborée": f"Canopy_Height_{epsg_num}.tif",
            "Raster de la catégorie hydrologique": f"Hydrologic_Soil_Group_{epsg_num}.tif",
            "Raster de la zone climatique (LCZ)": f"LCZ_{epsg_num}.tif",
            "Tableur en sortie" : f""
        }


        # Autocomplete button
        self.autocomplete_button = QPushButton("Activer Autocomplétion")
        self.autocomplete_button.clicked.connect(self.toggle_autocomplete)
        layout.addWidget(self.autocomplete_button)

        # Add form layout to main layout
        layout.addLayout(form_layout)

        # Add dialog buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)
        # Connect signals
        self.image_landsat_9.children()[2].clicked.connect(self.set_emprise_de_calcul)

        # self.epsg_widget.crsChanged.connect(self.on_epsg_changed)

        

    def toggle_autocomplete(self):
        self.autocomplete_enabled = not self.autocomplete_enabled
        if self.autocomplete_enabled:
            self.autocomplete_button.setText("Désactiver Autocomplétion")
            # Perform initial autocompletion
            self.autocomplete_paths()
        else:
            self.autocomplete_button.setText("Activer Autocomplétion")

    def reorganize_folder(self, first_file_path):
        # à tester car pour l'instant cela fonctionne lorsque les dossiers sont déjà créés mais cela pourrait beuguer s'il faut une création
        data_created = 0
        parent_dir_path = os.path.dirname(first_file_path)
        data_folder = "Data"
        results_folder = "Results"
        parent_parent_dir = os.path.dirname(parent_dir_path)
        print(parent_parent_dir)
        folder_dir = os.listdir(parent_parent_dir)
        if data_folder in folder_dir:
            print("Data folder already created")
            data_created = 1
        else : 
            data_folder_path = os.path.join(parent_dir_path,data_folder)
            os.makedirs(data_folder_path)
            for filename in os.listdir(parent_dir_path):
                file_path = os.path.join(parent_dir_path, filename)
                
                # Check if it is a file (not a directory)
                if os.path.isfile(file_path):
                    shutil.move(file_path, data_folder_path)

        if results_folder in folder_dir:
            print("Results folder already created")
        else : 
            results_folder_path = os.path.join(parent_dir_path,results_folder)
            os.makedirs(results_folder_path)

        if data_created:
            return parent_parent_dir
        else :
            return parent_dir_path
        

    
    def autocomplete_paths(self):
        first_file_path = self.image_landsat_9.children()[1].text()

        
        epsg = self.get_epsg_from_LST(first_file_path)
        print(epsg)
        self.update_label_to_filename(epsg)
        print(self.label_to_filename)
        self.epsg_widget.setCrs(QgsCoordinateReferenceSystem(f"EPSG:{epsg}"))

        if first_file_path:
            
    
            parent_dir_path = self.reorganize_folder(first_file_path)
            data_folder_path = os.path.join(parent_dir_path,"Data")
            results_folder_path = os.path.join(parent_dir_path,"Results")
            all_files = os.listdir(parent_dir_path)
            print(all_files)
            form_layout = self.layout().itemAt(1).layout()

            for i in range(form_layout.rowCount()):
                label_item = form_layout.itemAt(i, QFormLayout.LabelRole)
                field_item = form_layout.itemAt(i, QFormLayout.FieldRole)

                if label_item and field_item:
                    label_widget = label_item.widget()
                    field_widget = field_item.widget()

                    if label_widget and isinstance(label_widget, QLabel):
                        label_text = label_widget.text()
                        print(label_text)
                        print(self.label_to_filename)
                        if label_text in self.label_to_filename:
                            print(f"Label: {label_text}")
                            if isinstance(field_widget, QWidget):
                                line_edit = field_widget.findChild(QLineEdit)
                                print(line_edit)
                                if self.label_to_filename[label_text] != "" :
                                    line_edit.setText(os.path.join(data_folder_path,self.label_to_filename[label_text]))
                                else:
                                    dirname = parent_dir_path.split("/")[-1]
                                    city = dirname.split("_")[1:-1]
                                    city = "_".join(city)
                                    print(city)
                                    city_filename = make_csv(city)
                                    line_edit.setText(os.path.join(results_folder_path,city_filename))


    def get_epsg_from_LST(self,path):
        filename = path.split("/")[-1]
        name = filename.split(".")[0]
        epsg = name.split("_")[-1]
        return epsg


    def create_file_input(self):
        container = QHBoxLayout()
        line_edit = QLineEdit()
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.browse_file(line_edit))
        # container.addWidget(QLabel(label_text))
        container.addWidget(line_edit)
        container.addWidget(browse_button)
        widget = QWidget()
        widget.setLayout(container)
        return widget
    
    def create_file_output(self):
        container = QHBoxLayout()
        line_edit = QLineEdit()
        save_button = QPushButton("Save As")
        save_button.clicked.connect(lambda: self.save_file(line_edit))
        container.addWidget(line_edit)
        container.addWidget(save_button)
        widget = QWidget()
        widget.setLayout(container)
        return widget

    def save_file(self, line_edit):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save File As", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            line_edit.setText(file_path)

    
    def set_emprise_de_calcul(self):
        landsat_path = self.image_landsat_9.children()[1].text()
        epsg = self.get_epsg_from_LST(landsat_path)
    
        if landsat_path:
            try:
                landsat_layer = QgsRasterLayer(landsat_path, "Landsat Image")
                if landsat_layer.isValid():

                    target_crs = QgsCoordinateReferenceSystem('EPSG:4326')
                    original_crs = QgsCoordinateReferenceSystem(f'EPSG:{epsg}')
                    coordinate_transform = QgsCoordinateTransform(original_crs, target_crs, QgsProject.instance())
                    extent = landsat_layer.extent()
                    transform_extent = coordinate_transform.transformBoundingBox(extent)
                    print("transform extent", transform_extent)
                    self.emprise_de_calcul_de_luhi = transform_extent
                    print(self.emprise_de_calcul_de_luhi)
                else:
                    self.emprise_de_calcul_de_luhi.clear()
            except Exception as e:
                print(f"Error setting extent: {str(e)}")
    
    
    def update_label_to_filename(self, epsg_num):
        self.label_to_filename = {
            "Image LandSat 9" : f"LST_{epsg_num}.tif",
            "Raster du MNT": f"DEM_{epsg_num}.tif",
            "Raster de l'occupation du sol (DWV1)": f"Land_Cover_{epsg_num}.tif",
            "Raster de la nature du sol": f"Soil_Texture_{epsg_num}.tif",
            "Raster de la hauteur arborée": f"Canopy_Height_{epsg_num}.tif",
            "Raster de la catégorie hydrologique": f"Hydrologic_Soil_Group_{epsg_num}.tif",
            "Raster de la zone climatique (LCZ)": f"LCZ_{epsg_num}.tif",
            "Tableur en sortie" : ""
        }


    def browse_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Raster Files (*.tif *.tiff)")
        if file_path:
            line_edit.setText(file_path)
            if self.autocomplete_enabled:
                self.autocomplete_paths()

    def get_parameters(self):
        return {
            'image_landsat_9': self.image_landsat_9.children()[1].text(),
            'numro_de_bande_de_la_lst': self.numro_de_bande_de_la_lst.value(),
            'rsolution_de_la_couche_lst_m': self.rsolution_de_la_couche_lst_m.value(),
            'raster_du_mnt': self.raster_du_mnt.children()[1].text(),
            'raster_de_loccupation_du_sol_dwv1': self.raster_de_loccupation_du_sol_dwv1.children()[1].text(),
            'raster_de_la_nature_du_sol': self.raster_de_la_nature_du_sol.children()[1].text(),
            'raster_de_la_hauteur_arbore': self.raster_de_la_hauteur_arbore.children()[1].text(),
            'raster_de_la_catgorie_hydrologique': self.raster_de_la_catgorie_hydrologique.children()[1].text(),
            'raster_de_la_zone_climatique_lcz': self.raster_de_la_zone_climatique_lcz.children()[1].text(),
            'scr_de_projection_des_donnes': self.epsg_widget.crs(),
            'emprise_de_calcul_de_luhi': self.emprise_de_calcul_de_luhi,

            'nom_du_champ_daltitude': self.nom_du_champ_daltitude.text(),
            'nom_du_champ_de_nature_du_sol': self.nom_du_champ_de_nature_du_sol.text(),
            'nom_du_champ_de_pente': self.nom_du_champ_de_pente.text(),
            'nom_du_champ_dexposition': self.nom_du_champ_dexposition.text(),
            'nom_du_champ_doccupation_du_sol': self.nom_du_champ_doccupation_du_sol.text(),
            'nom_du_champ_pour_le_caractre_urbainrural': self.nom_du_champ_pour_le_caractre_urbainrural.text(),
            'nom_du_champ_de_hauteur_arbore': self.nom_du_champ_de_hauteur_arbore.text(),
            'nom_du_champ_de_catgorie_hydrologique': self.nom_du_champ_de_catgorie_hydrologique.text(),
            'nom_du_champ_de_zone_climatique': self.nom_du_champ_de_zone_climatique.text(),
            'nom_du_champ_dalbedo': self.nom_du_champ_dalbedo.text(),
            'tableur_sortie' : self.tableur_sortie.children()[1].text()
        }

if __name__ == '__main__':

    app = QApplication(sys.argv)
    dialog = InputDialog()

    Processing.initialize()


    if dialog.exec_() == QDialog.Accepted:
        parameters = dialog.get_parameters()
        print(parameters)  # For testing, print the parameters

        # Use the parameters to run your QGIS processing algorithm
        algorithm = ExtractionDuFichierCsvPourOutilIa()
        context = QgsProcessingContext()
        feedback = QgsProcessingFeedback()

        result = algorithm.processAlgorithm(parameters, context, feedback)
