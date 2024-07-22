"""
Model exported as python.
Name : Modification d'un csv pour intégrer une nouvelle zone urbaine
Group : 
With QGIS : 33603
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class ModificationDunCsvPourIntgrerUneNouvelleZoneUrbaine(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('couche_des_points_de_ltat_actuel', "Couche des points de l'état actuel", types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('couche_des_polygones_durbanisation_future', "Couche des polygones d'urbanisation future", types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('champ_de_lalbedo_futur', "Champ de l'albedo futur", type=QgsProcessingParameterField.Any, parentLayerParameterName='couche_des_polygones_durbanisation_future', allowMultiple=False, defaultValue='ALBFUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('TableurDesPointsMisJour', 'Tableur des points mis à jour', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}

        # Extraction des points à modifier
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': parameters['couche_des_points_de_ltat_actuel'],
            'JOIN': parameters['couche_des_polygones_durbanisation_future'],
            'JOIN_FIELDS': parameters['champ_de_lalbedo_futur'],
            'METHOD': 1,  # Prendre uniquement les attributs de la première entité correspondante (un à un)
            'PREDICATE': [5],  # est à l'intérieur
            'PREFIX': None,
            'NON_MATCHING': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractionDesPointsModifier'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Mise à jour de l'albedo
        alg_params = {
            'FIELD_LENGTH': 23,
            'FIELD_NAME': 'ALB',
            'FIELD_PRECISION': 15,
            'FIELD_TYPE': 0,  # Décimal (double)
            'FORMULA': ' attribute( $currentfeature , @champ_de_lalbedo_futur )',
            'INPUT': outputs['ExtractionDesPointsModifier']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MiseJourDeLalbedo'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Mise à jour de la hauteur arborée
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'HAUTA',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': '0',
            'INPUT': outputs['MiseJourDeLalbedo']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MiseJourDeLaHauteurArbore'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Mise à jour du caractère urbain
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'URB',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': '1',
            'INPUT': outputs['MiseJourDeLalbedo']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MiseJourDuCaractreUrbain'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Mise à jour de l'occupation du sol
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'OCCSOL',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entier (32bit)
            'FORMULA': '6',
            'INPUT': outputs['MiseJourDeLaHauteurArbore']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MiseJourDeLoccupationDuSol'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Fusion des points modifiés avec les autres
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['ExtractionDesPointsModifier']['NON_MATCHING'],outputs['MiseJourDeLoccupationDuSol']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FusionDesPointsModifisAvecLesAutres'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Suppression du champ temporaire d'albedo
        alg_params = {
            'COLUMN': parameters['champ_de_lalbedo_futur'],
            'INPUT': outputs['FusionDesPointsModifisAvecLesAutres']['OUTPUT'],
            'OUTPUT': parameters['TableurDesPointsMisJour']
        }
        outputs['SuppressionDuChampTemporaireDalbedo'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TableurDesPointsMisJour'] = outputs['SuppressionDuChampTemporaireDalbedo']['OUTPUT']
        return results

    def name(self):
        return "Modification d'un csv pour intégrer une nouvelle zone urbaine"

    def displayName(self):
        return "Modification d'un csv pour intégrer une nouvelle zone urbaine"

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return ModificationDunCsvPourIntgrerUneNouvelleZoneUrbaine()
