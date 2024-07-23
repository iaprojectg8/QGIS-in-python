"""
Model exported as python.
Name : Extraction du fichier csv pour outil IA
Group : UHI
With QGIS : 33603
"""


from utils.imports import  *
from utils.variables import *


class ExtractionDuFichierCsvPourOutilIa(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('image_landsat_9', 'Image LandSat 9', defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('numro_de_bande_de_la_lst', 'Numéro de bande de la LST', type=QgsProcessingParameterNumber.Integer, minValue=1, defaultValue=7))
        self.addParameter(QgsProcessingParameterNumber('rsolution_de_la_couche_lst_m', 'Résolution de la couche LST (m)', type=QgsProcessingParameterNumber.Double, minValue=0, defaultValue=30))
        self.addParameter(QgsProcessingParameterRasterLayer('raster_du_mnt', 'Raster du MNT', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('raster_de_loccupation_du_sol_dwv1', "Raster de l'occupation du sol (DWV1)", defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('raster_de_la_nature_du_sol', 'Raster de la nature du sol', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('raster_de_la_hauteur_arbore', 'Raster de la hauteur arborée', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('raster_de_la_catgorie_hydrologique', 'Raster de la catégorie hydrologique', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('raster_de_la_zone_climatique_lcz', 'Raster de la zone climatique (LCZ)', defaultValue=None))
        self.addParameter(QgsProcessingParameterCrs('scr_de_projection_des_donnes', 'SCR de projection des données', defaultValue='EPSG:32629'))
        self.addParameter(QgsProcessingParameterExtent('emprise_de_calcul_de_luhi', "Emprise de calcul de l'UHI", defaultValue=None))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_daltitude', "Nom du champ d'altitude", multiLine=False, defaultValue='ALT'))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_de_nature_du_sol', 'Nom du champ de nature du sol', multiLine=False, defaultValue='NATSOL'))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_de_pente', 'Nom du champ de pente', multiLine=False, defaultValue='PENTE'))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_dexposition', "Nom du champ d'exposition", multiLine=False, defaultValue='EXP'))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_doccupation_du_sol', "Nom du champ d'occupation du sol", multiLine=False, defaultValue='OCCSOL'))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_pour_le_caractre_urbainrural', 'Nom du champ pour le caractère urbain-rural', multiLine=False, defaultValue='URB'))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_de_hauteur_arbore', 'Nom du champ de hauteur arborée', multiLine=False, defaultValue='HAUTA'))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_de_catgorie_hydrologique', 'Nom du champ de catégorie hydrologique', multiLine=False, defaultValue='CATHYD'))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_de_zone_climatique', 'Nom du champ de zone climatique', multiLine=False, defaultValue='ZONECL'))
        self.addParameter(QgsProcessingParameterString('nom_du_champ_dalbedo', "Nom du champ d'albedo", multiLine=False, defaultValue='ALB'))
        self.addParameter(QgsProcessingParameterFeatureSink('tableur_sortie', 'Tableur en sortie', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        print(parameters)
        feedback = QgsProcessingMultiStepFeedback(43, model_feedback)
        results = {}
        outputs = {}
        source_crs = parameters['scr_de_projection_des_donnes']
        target_crs = QgsCoordinateReferenceSystem('EPSG:4326')

        # Reprojection de la catégorie hydrologique
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': parameters['raster_de_la_catgorie_hydrologique'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': None,
            'RESAMPLING': 0,  # Plus Proche Voisin
            'SOURCE_CRS': source_crs,
            'TARGET_CRS': target_crs,
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectionDeLaCatgorieHydrologique'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Reprojection done")
    
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Reprojection de la nature du sol
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': parameters['raster_de_la_nature_du_sol'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': None,
            'RESAMPLING': 0,  # Plus Proche Voisin
            'SOURCE_CRS': source_crs,
            'TARGET_CRS': target_crs,
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectionDeLaNatureDuSol'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Reprojection done")
    
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Reprojection du MNT
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': parameters['raster_du_mnt'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': None,
            'RESAMPLING': 0,  # Plus Proche Voisin
            'SOURCE_CRS': source_crs,
            'TARGET_CRS': target_crs,
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectionDuMnt'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Reprojection done")
    
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Reprojection de la hauteur arborée
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': parameters['raster_de_la_hauteur_arbore'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': None,
            'RESAMPLING': 0,  # Plus Proche Voisin
            'SOURCE_CRS': source_crs,
            'TARGET_CRS': target_crs,
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectionDeLaHauteurArbore'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Reprojection done")
    

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Découpage de la nature du sol
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': outputs['ReprojectionDeLaNatureDuSol']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': None,
            'OVERCRS': False,
            'PROJWIN': parameters['emprise_de_calcul_de_luhi'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DcoupageDeLaNatureDuSol'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Landcover cut done")
    
        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Découpage du MNT
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': outputs['ReprojectionDuMnt']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': None,
            'OVERCRS': False,
            'PROJWIN': parameters['emprise_de_calcul_de_luhi'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DcoupageDuMnt'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("DEM cut done")
    
        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Découpage de la catégorie hydrologique
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': outputs['ReprojectionDeLaCatgorieHydrologique']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': None,
            'OVERCRS': False,
            'PROJWIN': parameters['emprise_de_calcul_de_luhi'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DcoupageDeLaCatgorieHydrologique'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Cut done")
    
        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Reprojection de l'occupation du sol
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': parameters['raster_de_loccupation_du_sol_dwv1'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': None,
            'RESAMPLING': 0,  # Plus Proche Voisin
            'SOURCE_CRS': source_crs,
            'TARGET_CRS': target_crs,
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectionDeLoccupationDuSol'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Reprojection done")
    
        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Reprojection de l'image LandSat
        alg_params = {
            'DATA_TYPE': 6,  # Float32
            'EXTRA': None,
            'INPUT': parameters['image_landsat_9'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': None,
            'RESAMPLING': 0,  # Plus Proche Voisin
            'SOURCE_CRS': source_crs,
            'TARGET_CRS': target_crs,
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectionDeLimageLandsat'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Reprojection done")
    
        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Découpage de la hauteur arborée
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': outputs['ReprojectionDeLaHauteurArbore']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': None,
            'OVERCRS': False,
            'PROJWIN': parameters['emprise_de_calcul_de_luhi'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DcoupageDeLaHauteurArbore'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Cut done")
    
        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}
        
        # Reprojection de la zone climatique
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': parameters['raster_de_la_zone_climatique_lcz'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': None,
            'RESAMPLING': 0,  # Plus Proche Voisin
            'SOURCE_CRS': source_crs,
            'TARGET_CRS': target_crs,
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectionDeLaZoneClimatique'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Reprojection done")
    
        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Découpage de l'image LandSat
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': outputs['ReprojectionDeLimageLandsat']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': None,
            'OVERCRS': False,
            'PROJWIN': parameters['emprise_de_calcul_de_luhi'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DcoupageDeLimageLandsat'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Cut done")

        alg_params_rearrange = {
            'INPUT': outputs['ReprojectionDeLimageLandsat']['OUTPUT'],
            'BANDS': [1, 2, 3, 4, 5, 6],  # Exclude the 7th band
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs["BandSelection"] = processing.run('gdal:rearrange_bands', alg_params_rearrange, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rearranged raster")
        # Découpage de l'image LandSat
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': outputs["BandSelection"]["OUTPUT"],
            'NODATA': None,
            'OPTIONS': None,
            'OVERCRS': False,
            'PROJWIN': parameters['emprise_de_calcul_de_luhi'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DcoupageLS'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Decoupage ls done")
        # feedback.setCurrentStep(12)
        # if feedback.isCanceled():
        #     return {}

        # Calcul de l'exposition
        alg_params = {
            'BAND': 1,
            'COMPUTE_EDGES': True,
            'EXTRA': None,
            'INPUT': outputs['DcoupageDuMnt']['OUTPUT'],
            'OPTIONS': None,
            'TRIG_ANGLE': False,
            'ZERO_FLAT': True,
            'ZEVENBERGEN': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        filepath = outputs["DcoupageDuMnt"]["OUTPUT"]
        if os.path.exists(filepath):
            print(f"The file '{filepath}' exists.")
        else:
            print(f"The file '{filepath}' does not exist.")
        
        
        outputs['CalculDeLexposition'] = processing.run('gdal:aspect', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Calculus done")
    
        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Vectorisation de l'image LandSat 9 (LST)
        alg_params = {
            'FIELD_NAME': 'LST',
            'INPUT_RASTER': outputs['DcoupageDeLimageLandsat']['OUTPUT'],
            'RASTER_BAND': parameters['numro_de_bande_de_la_lst'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['VectorisationDeLimageLandsat9Lst'] = processing.run('native:pixelstopoints', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Vectorization done")
    
        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Calcul de la pente
        alg_params = {
            'AS_PERCENT': True,
            'BAND': 1,
            'COMPUTE_EDGES': True,
            'EXTRA': None,
            'INPUT': outputs['DcoupageDuMnt']['OUTPUT'],
            'OPTIONS': None,
            'SCALE': 1,
            'ZEVENBERGEN': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculDeLaPente'] = processing.run('gdal:slope', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Calculus done")
        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Découpage de l'occupation du sol
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': outputs['ReprojectionDeLoccupationDuSol']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': None,
            'OVERCRS': False,
            'PROJWIN': parameters['emprise_de_calcul_de_luhi'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DcoupageDeLoccupationDuSol'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Cut done")
        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Découpage de la zone climatique
        alg_params = {
            'DATA_TYPE': 0,  # Utiliser le type de donnée de la couche en entrée
            'EXTRA': None,
            'INPUT': outputs['ReprojectionDeLaZoneClimatique']['OUTPUT'],
            'NODATA': None,
            'OPTIONS': None,
            'OVERCRS': False,
            'PROJWIN': parameters['emprise_de_calcul_de_luhi'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DcoupageDeLaZoneClimatique'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Cut  done")
        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}


        # Ajouter les champs X/Y à la couche
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'INPUT': outputs['VectorisationDeLimageLandsat9Lst']['OUTPUT'],
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjouterLesChampsXyLaCouche'] = processing.run('native:addxyfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("X and y done")
        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        

        # Renommage du champ y
        alg_params = {
            'FIELD': 'y',
            'INPUT': outputs['AjouterLesChampsXyLaCouche']['OUTPUT'],
            'NEW_NAME': 'LAT',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommageDuChampY'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rename done")
        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Renommage du champ x
        alg_params = {
            'FIELD': 'x',
            'INPUT': outputs['RenommageDuChampY']['OUTPUT'],
            'NEW_NAME': 'LON',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommageDuChampX'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rename done")
        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Extraction des bandes LandSat
        alg_params = {
            'COLUMN_PREFIX': 'LS',
            'INPUT': outputs['RenommageDuChampX']['OUTPUT'],
            'RASTERCOPY': outputs['DcoupageLS']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDesBandesLandsat'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Extraction done")
        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Extraction de l'occupation du sol
        alg_params = {
            'COLUMN_PREFIX': parameters['nom_du_champ_doccupation_du_sol'],
            'INPUT': outputs['ExtractionDesBandesLandsat']['OUTPUT'],
            'RASTERCOPY': outputs['DcoupageDeLoccupationDuSol']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDeLoccupationDuSol'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Extraction done")
        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Renommage du champ d'occupation du sol
        alg_params = {
            'FIELD': parameters['nom_du_champ_doccupation_du_sol'] + '1',
            'INPUT': outputs['ExtractionDeLoccupationDuSol']['OUTPUT'],
            'NEW_NAME': parameters['nom_du_champ_doccupation_du_sol'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommageDuChampDoccupationDuSol'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rename done")
        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Extraction du caractère Urbain-Rural
        alg_params = {
            'FIELD_LENGTH': 25,
            'FIELD_NAME': parameters['nom_du_champ_pour_le_caractre_urbainrural'],
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': 'CASE WHEN attribute( $currentfeature ,  @nom_du_champ_doccupation_du_sol ) = 6 THEN 1\r\nELSE 0\r\nEND',
            'INPUT': outputs['RenommageDuChampDoccupationDuSol']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDuCaractreUrbainrural'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Extraction done")
        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Extraction de l'altitude
        alg_params = {
            'COLUMN_PREFIX': parameters['nom_du_champ_daltitude'],
            'INPUT': outputs['ExtractionDuCaractreUrbainrural']['OUTPUT'],
            'RASTERCOPY': outputs['DcoupageDuMnt']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDeLaltitude'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Extraction lat done")
        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Renommage du champ d'altitude
        alg_params = {
            'FIELD': parameters['nom_du_champ_daltitude'] + '1',
            'INPUT': outputs['ExtractionDeLaltitude']['OUTPUT'],
            'NEW_NAME': parameters['nom_du_champ_daltitude'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommageDuChampDaltitude'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Reanme lat done")
        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Extraction de l'exposition
        alg_params = {
            'COLUMN_PREFIX': parameters['nom_du_champ_dexposition'],
            'INPUT': outputs['RenommageDuChampDaltitude']['OUTPUT'],
            'RASTERCOPY': outputs['CalculDeLexposition']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDeLexposition'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Extraction expo done")
        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Renommage du champ d'exposition
        alg_params = {
            'FIELD': parameters['nom_du_champ_dexposition'] + str(1),
            'INPUT': outputs['ExtractionDeLexposition']['OUTPUT'],
            'NEW_NAME': parameters['nom_du_champ_dexposition'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommageDuChampDexposition'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rename done")
        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Extraction de la pente
        alg_params = {
            'COLUMN_PREFIX': parameters['nom_du_champ_de_pente'],
            'INPUT': outputs['RenommageDuChampDexposition']['OUTPUT'],
            'RASTERCOPY': outputs['CalculDeLaPente']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDeLaPente'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Exraction pente done")
        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Renommage du champ de pente
        alg_params = {
            'FIELD': parameters['nom_du_champ_de_pente'] + '1',
            'INPUT': outputs['ExtractionDeLaPente']['OUTPUT'],
            'NEW_NAME': parameters['nom_du_champ_de_pente'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommageDuChampDePente'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rename pente done")
        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Extraction de la nature du sol
        alg_params = {
            'COLUMN_PREFIX': parameters['nom_du_champ_de_nature_du_sol'],
            'INPUT': outputs['RenommageDuChampDePente']['OUTPUT'],
            'RASTERCOPY': outputs['DcoupageDeLaNatureDuSol']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDeLaNatureDuSol'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Extraction natsol done")
        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Renommage du champ de nature du sol
        alg_params = {
            'FIELD': parameters['nom_du_champ_de_nature_du_sol'] + '1',
            'INPUT': outputs['ExtractionDeLaNatureDuSol']['OUTPUT'],
            'NEW_NAME': parameters['nom_du_champ_de_nature_du_sol'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommageDuChampDeNatureDuSol'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rename natsol done")
        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Extraction de la hauteur arborée
        alg_params = {
            'COLUMN_PREFIX': parameters['nom_du_champ_de_hauteur_arbore'],
            'INPUT': outputs['RenommageDuChampDeNatureDuSol']['OUTPUT'],
            'RASTERCOPY': outputs['DcoupageDeLaHauteurArbore']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDeLaHauteurArbore'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Extract hauteur arbre done")
        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Renommage du champ de hauteur arborée
        alg_params = {
            'FIELD': parameters['nom_du_champ_de_hauteur_arbore'] + '1',
            'INPUT': outputs['ExtractionDeLaHauteurArbore']['OUTPUT'],
            'NEW_NAME': parameters['nom_du_champ_de_hauteur_arbore'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommageDuChampDeHauteurArbore'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rename hauta done")
        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Extraction de la catégorie hydrologique
        alg_params = {
            'COLUMN_PREFIX': parameters['nom_du_champ_de_catgorie_hydrologique'],
            'INPUT': outputs['RenommageDuChampDeHauteurArbore']['OUTPUT'],
            'RASTERCOPY': outputs['DcoupageDeLaCatgorieHydrologique']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDeLaCatgorieHydrologique'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Extraction cathyd done")
        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Renommage du champ de catégorie hydrologique
        alg_params = {
            'FIELD': parameters['nom_du_champ_de_catgorie_hydrologique'] + '1',
            'INPUT': outputs['ExtractionDeLaCatgorieHydrologique']['OUTPUT'],
            'NEW_NAME': parameters['nom_du_champ_de_catgorie_hydrologique'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenommageDuChampDeCatgorieHydrologique'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rename cathyd done")
        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # Extraction de la zone climatique
        alg_params = {
            'COLUMN_PREFIX': parameters['nom_du_champ_de_zone_climatique'],
            'INPUT': outputs['RenommageDuChampDeCatgorieHydrologique']['OUTPUT'],
            'RASTERCOPY': outputs['DcoupageDeLaZoneClimatique']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDeLaZoneClimatique'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Extract zoncli done")
        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Renommage du champ de zone climatique
        alg_params = {
            'FIELD': parameters['nom_du_champ_de_zone_climatique'] + '1',
            'INPUT': outputs['ExtractionDeLaZoneClimatique']['OUTPUT'],
            'NEW_NAME': parameters['nom_du_champ_de_zone_climatique'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        
        outputs['RenommageDuChampDeZoneClimatique'] = processing.run ('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Rename zonecli done")
        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Suppression des points avec données attributaires "nan"

        conditions = ["LST <> 0 AND EXP <> '-nan(ind)'"]
        for field in FIELDS:

            conditions.append(f"{field} IS NOT NULL")
            conditions.append(f"{field} <> 'nan'")

        # Join all conditions with 'AND'
        expression = ' AND '.join(conditions)
        print(expression)
        
        alg_params = {
        
            'EXPRESSION': f"{expression}",
            'INPUT': outputs['RenommageDuChampDeZoneClimatique']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesPointsAvecDonnesAttributairesNan'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        print("Delete nan done")
        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # Calcul de l'albedo
       
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': parameters['nom_du_champ_dalbedo'],
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': '((0.356*"LS1") + (0.130*"LS3") + (0.373*"LS4") + (0.085*"LS5") + (0.072*"LS6") -0.018) / 1.016',
            'INPUT': outputs['SuppressionDesPointsAvecDonnesAttributairesNan']['OUTPUT'],
            'OUTPUT': parameters['tableur_sortie']
        }
        outputs['CalculDeLalbedo'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        print("CSV generated")
        results['TableurEnSortie'] = outputs['CalculDeLalbedo']['OUTPUT']
        return results

    def name(self):
        return 'Extraction du fichier csv pour outil IA'

    def displayName(self):
        return 'Extraction du fichier csv pour outil IA'

    def group(self):
        return 'UHI'

    def groupId(self):
        return 'UHI'

    def createInstance(self):
        return ExtractionDuFichierCsvPourOutilIa()
