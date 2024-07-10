# app/services/profiling_strategy.py
from abc import ABC, abstractmethod

class DataProfilingStrategy(ABC):
    @abstractmethod
    def generate_profile(self, data):
        pass

class YDataProfilingStrategy(DataProfilingStrategy):
    def generate_profile(self, data):
        import ydata_profiling
        profile = ydata_profiling.ProfileReport(data)
        return profile

# Example for another library (future implementation)
# class AnotherLibraryProfilingStrategy(DataProfilingStrategy):
#     def generate_profile(self, data):
#         # Replace with actual implementation
#         profile = SomeOtherLibrary.ProfileReport(data)
#         return profile
