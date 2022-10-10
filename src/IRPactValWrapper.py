from metaheuristic_algorithms.function_wrappers.abstract_wrapper import AbstractWrapper
import configuration
import simulationRunner

class IRPactValWrapperMAE(AbstractWrapper):

    def maximum_decision_variable_values(self):
        return [configuration.optimizationBounds['maxAdoptionThreshold'], configuration.optimizationBounds['maxInterestThreshold']]

    def minimum_decision_variable_values(self):
        return [configuration.optimizationBounds['minAdoptionThreshold'],
                configuration.optimizationBounds['minInterestThreshold']]

    def objective_function_value(self, decision_variable_values, model):
            simulationRunner.prepareJson(configuration.templateFile, decision_variable_values[0], decision_variable_values[1], configuration.defaultInputFile)
            return simulationRunner.invokeJar(configuration.templateFile + '-' + str(decision_variable_values[0])[2:len(str(decision_variable_values[0]))] + "-" + str(decision_variable_values[1]), 'MAE', model)

    def initial_decision_variable_value_estimates(self):
        return [configuration.optimizationStartValues[0], configuration.optimizationStartValues[1]]


class IRPactValWrapperRMSE(AbstractWrapper):

    def maximum_decision_variable_values(self):
        return [configuration.optimizationBounds['maxAdoptionThreshold'], configuration.optimizationBounds['maxInterestThreshold']]

    def minimum_decision_variable_values(self):
        return [configuration.optimizationBounds['minAdoptionThreshold'],
                configuration.optimizationBounds['minInterestThreshold']]

    def objective_function_value(self, decision_variable_values):
            simulationRunner.prepareJson(configuration.templateFile, decision_variable_values[0], decision_variable_values[1], configuration.defaultInputFile)
            return simulationRunner.invokeJar(configuration.templateFile + '-' + str(decision_variable_values[0])[2:len(str(decision_variable_values[0]))] + "-" + str(decision_variable_values[1]), 'RMSE')

    def initial_decision_variable_value_estimates(self):
        return [configuration.optimizationStartValues[0], configuration.optimizationStartValues[1]]

# TODO remove ugly hack with hardcoding the AT
class IRPactValWrapperMAESingleVariable(AbstractWrapper):

    def maximum_decision_variable_values(self):
        return [configuration.optimizationBounds['maxAdoptionThreshold']]

    def minimum_decision_variable_values(self):
        return [configuration.optimizationBounds['minAdoptionThreshold']]

    def objective_function_value(self, decision_variable_values):
            simulationRunner.prepareJsonDefaultIT(configuration.templateFile, decision_variable_values, configuration.defaultInterestThreshold)
            return simulationRunner.invokeJar(configuration.templateFile + '-' + str(decision_variable_values)[2:len(str(decision_variable_values))] + "-" + str(configuration.defaultInterestThreshold), 'MAE')

    def initial_decision_variable_value_estimates(self):
        return configuration.optimizationStartValues['adoptionThreshold']

# TODO remove ugly hack with hardcoding the AT
class IRPactValWrapperRMSESingleVariable(AbstractWrapper):

    def maximum_decision_variable_values(self):
        return [configuration.optimizationBounds['maxAdoptionThreshold']]

    def minimum_decision_variable_values(self):
        return [configuration.optimizationBounds['minAdoptionThreshold']]

    def objective_function_value(self, decision_variable_values):
            simulationRunner.prepareJsonDefaultIT(configuration.templateFile, decision_variable_values, configuration.defaultInterestThreshold)
            return simulationRunner.invokeJar(configuration.templateFile + '-' + str(decision_variable_values)[2:len(str(decision_variable_values))] + "-" + str(configuration.defaultInterestThreshold), 'RMSD')

    def initial_decision_variable_value_estimates(self):
        return configuration.optimizationStartValues['adoptionThreshold']
