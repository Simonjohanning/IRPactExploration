import random

from metaheuristic_algorithms.function_wrappers.abstract_wrapper import AbstractWrapper
import configurationPVact
import simulationRunner

class PVactWrapperMAE(AbstractWrapper):
    """
    Class to provide a Wrapper for the mean average value metric used for evaluating model within metaheuristics
    """

    def maximum_decision_variable_values(self):
        return [configurationPVact.optimizationBounds['maxAdoptionThreshold'], configurationPVact.optimizationBounds['maxInterestThreshold']]

    def minimum_decision_variable_values(self):
        return [configurationPVact.optimizationBounds['minAdoptionThreshold'],
                configurationPVact.optimizationBounds['minInterestThreshold']]

    def objective_function_value(self, decision_variable_values, model):
            simulationRunner.prepareJson(configurationPVact.templateFile, decision_variable_values[0], decision_variable_values[1], configurationPVact.defaultInputFile)
            return simulationRunner.invokeJar(configurationPVact.templateFile + '-' + str(decision_variable_values[0])[2:len(str(decision_variable_values[0]))] + "-" + str(decision_variable_values[1]), 'MAE', model)

    def initial_decision_variable_value_estimates(self):
        return [configurationPVact.optimizationStartValues[0], configurationPVact.optimizationStartValues[1]]


class PVactWrapperRMSE(AbstractWrapper):
    """
    Class to provide a Wrapper for the root mean square average value metric used for evaluating model within metaheuristics
    """
    def maximum_decision_variable_values(self):
        return [configurationPVact.optimizationBounds['maxAdoptionThreshold'], configurationPVact.optimizationBounds['maxInterestThreshold']]

    def minimum_decision_variable_values(self):
        return [configurationPVact.optimizationBounds['minAdoptionThreshold'],
                configurationPVact.optimizationBounds['minInterestThreshold']]

    def objective_function_value(self, decision_variable_values):
            simulationRunner.prepareJson(configurationPVact.templateFile, decision_variable_values[0], decision_variable_values[1], configurationPVact.defaultInputFile)
            return simulationRunner.invokeJar(configurationPVact.templateFile + '-' + str(decision_variable_values[0])[2:len(str(decision_variable_values[0]))] + "-" + str(decision_variable_values[1]), 'RMSE')

    def initial_decision_variable_value_estimates(self):
        return [configurationPVact.optimizationStartValues[0], configurationPVact.optimizationStartValues[1]]

# TODO remove ugly hack with hardcoding the AT
class PVactWrapperMAESingleVariable(AbstractWrapper):
    """
    Class to provide a Wrapper for the mean average value metric with a single variable used for evaluating model within metaheuristics
    """
    def maximum_decision_variable_values(self):
        return [configurationPVact.optimizationBounds['maxAdoptionThreshold']]

    def minimum_decision_variable_values(self):
        return [configurationPVact.optimizationBounds['minAdoptionThreshold']]

    def objective_function_value(self, decision_variable_values):
            simulationRunner.prepareJson(configurationPVact.templateFile, 'model', {'adoptionThreshold': decision_variable_values, 'interestThreshold': configurationPVact.defaultInterestThreshold, 'AP': configurationPVact.gds_defaults['AP'], 'IP': configurationPVact.gds_defaults['IP'], 'currentSeed': random.randint(0, 99999)})
            return simulationRunner.invokeJar(configurationPVact.templateFile + '-' + str(decision_variable_values)[2:len(str(decision_variable_values))] + "-" + str(configuration.defaultInterestThreshold), 'MAE')

    def initial_decision_variable_value_estimates(self):
        return configurationPVact.optimizationStartValues['adoptionThreshold']

# TODO remove ugly hack with hardcoding the AT
class PVactWrapperRMSESingleVariable(AbstractWrapper):
    """
        Class to provide a Wrapper for the root mean square average value metric with a single variable used for evaluating model within metaheuristics
    """
    def maximum_decision_variable_values(self):
        return [configurationPVact.optimizationBounds['maxAdoptionThreshold']]

    def minimum_decision_variable_values(self):
        return [configurationPVact.optimizationBounds['minAdoptionThreshold']]

    def objective_function_value(self, decision_variable_values):
            simulationRunner.prepareJson(configurationPVact.templateFile, 'PVact', {'adoptionThreshold': decision_variable_values, 'interestThreshold': configurationPVact.defaultInterestThreshold, 'AP': configurationPVact.gds_defaults['AP'], 'IP': configurationPVact.gds_defaults['IP'], 'currentSeed': random.randint(0, 99999)})
            return simulationRunner.invokeJar(configurationPVact.templateFile + '-' + str(decision_variable_values)[2:len(str(decision_variable_values))] + "-" + str(configurationPVact.defaultInterestThreshold), 'RMSD')

    def initial_decision_variable_value_estimates(self):
        return configurationPVact.optimizationStartValues['adoptionThreshold']
