import unittest
from caseparser import CaseParser
from string import printable
from time import time

class TestCaseParser(unittest.TestCase):
    def setUp(self):
        self.start_time()
        self.seps = [p for p in printable if not p.isalnum()]
        self.seps.pop(23)
        self.seps.append('')
        self.CP = CaseParser()
        self.test_cases = [
                "simpleTestString",  # Simple string with no special characters
                "AnotherSimpleTest123",  # String with numbers
                "This_is_a_Test_String_with_Underscores",  # String with underscores
                "StringWith---Multiple-Hyphens",  # String with multiple hyphens
                "MiXeD_CaSe_And123Numbers456",  # String with mixed case and numbers
                "randomSTRING_withVARIOUS@@symbols&&andNumbers1234",  # String with various symbols and numbers
                "moreComplexStringWith#Various_SymbolsAnd_MixedCases567",  # String with more complex mix of symbols and cases
                "aVery---LongString_withLots__OfDifferentCharacters_1234567890",  # Long string with many different characters
                "shortString!@#",  # Short string with special characters
                "finalTestString_With123Numbers_andSymbols*&^%$#@",  # Final string with numbers and a variety of symbols
                "ExtraComplexString_with**Multiple_Separators_andNumbers6789",  # Extra complex string with multiple separators
                "NoisyStringWith@@@@Lots$$$of%%%Special###Characters",  # Noisy string with many special characters
                "UnderScore_Heavy__String_With_MixedCases_andNumbers987",  # String with heavy underscores
                "CapsLOCKStringWITHMixedCAPS_and_NUMBERS4321",  # String with mixed capitalization
                "longStringWithVariety123_andSpecialCharacters!@#$%^",  # Long string with variety and special characters
                "simpleMixedString_withNumbers1234andLetters",  # Simple mixed string with numbers and letters extra
                "another---example_with_Mixed!@#cases_and123Numbers",  # Another example with mixed cases and symbols
                "shortAndSweet12345",  # Short string with numbers
                "superLONGStringWithALotOfDifferentTypesOfCharacters1234567890",  # Super long string with many types
                "finalExample_String-with_Many**Kinds++of&&Symbols_and123Numbers",  # Final example with many kinds of symbols and numbers
                "The room was a disaster zone, with clothes strewn across the floor like a colorful patchwork quilt tossed by a hurricane. Empty soda cans and crumpled snack wrappers littered every available surface, while textbooks and notebooks lay scattered about in haphazard piles. The once-pristine whiteboard was now covered in a chaotic jumble of equations and doodles, with eraser dust forming a fine layer over everything. The air was thick with the scent of stale pizza and sweat, and the sound of a buzzing fly added to the cacophony. Amidst the chaos, a lone laptop sat precariously on the edge of a cluttered desk, its screen flickering intermittently as if struggling to stay alive amidst the chaos."
            ]
        self.test_camel_truth = [
                "simpleTestString",
                "anotherSimpleTest123",
                "thisIsATestStringWithUnderscores",
                "stringWithMultipleHyphens",
                "mixedCaseAnd123Numbers456",
                "randomStringWithVariousSymbolsAndNumbers1234",
                "moreComplexStringWithVariousSymbolsAndMixedCases567",
                "aVeryLongStringWithLotsOfDifferentCharacters1234567890",
                "shortString",
                "finalTestStringWith123NumbersAndSymbols",
                "extraComplexStringWithMultipleSeparatorsAndNumbers6789",
                "noisyStringWithLotsOfSpecialCharacters",
                "underscoreHeavyStringWithMixedCasesAndNumbers987",
                "capsLockStringWithMixedCapsAndNumbers4321",
                "longStringWithVariety123AndSpecialCharacters",
                "simpleMixedStringWithNumbers1234AndLetters",
                "anotherExampleWithMixedCasesAnd123Numbers",
                "shortAndSweet12345",
                "superLongStringWithALotOfDifferentTypesOfCharacters1234567890",
                "finalExampleStringWithManyKindsOfSymbolsAnd123Numbers",
                "theRoomWasADisasterZoneWithClothesStrewnAcrossTheFloorLikeAColorfulPatchWorkQuiltTossedByAHurricaneEmptySodaCansAndCrumpledSnackWrappersLitteredEveryAvailableSurfaceWhileTextbooksAndNotebooksLayScatteredAboutInHaphazardPilesTheOncePristineWhiteBoardWasNowCoveredInAChaoticJumbleOfEquationsAndDoodlesWithEraserDustFormingAFineLAyeRoverEverythingTheAirWasThickWithTheScentOfStalePizzaAndSweatAndTheSoundOfABuzzIngFlyAddedToTheCacophonyAmidstTheChaosAloneLaptopSatPrecariouslyONTheEdgeOfAClutteredDesKitsScreenFlickeringIntermittentlyAsIfStrugglingToStayAliveAmidstTheChaos"
        ]

    def start_time(self):
        self.timer = time()

    def get_time(self):
        _ct = time() - self.timer
        self.start_time()

        return f'\n{format(_ct, ".4")} seconds to test\n' + \
               f'{len(self.seps)* len(self.test_cases) * (len(list(self.CP.__cases__.keys())) + 1)} string normalizations.\n' + \
               f'Separators: {len(self.seps)}\n' + \
               f'Test Strings: {len(self.test_cases)}\n' + \
               f'Cases: {list(self.CP.__cases__.keys()) + ["drop_vowels"]}'
    
    def test_camel_case_parse(self):
        self.start_time()
        for sep in self.seps:
            strings = self.CP.parse(self.test_cases, sep=sep, casing='camel', drop_vowels=False)
            self.assertTrue(strings[0][0].islower() or strings[0][0].isdecimal())
            for s in strings:
                self.assertNotRegex(s, r'([^a-zA-Z0-9' + sep + '])')
                if sep == '':
                    self.assertTrue(s in self.test_camel_truth)
        print(self.get_time())

    def test_lower_case_parse(self):
        self.start_time()
        for sep in self.seps:
            strings = self.CP.parse(self.test_cases, sep=sep, casing='lower', drop_vowels=False)
            self.assertTrue(word.islower() for word in strings)
            for s in strings:
                self.assertNotRegex(s, r'([^a-zA-Z0-9' + sep + '])')
        print(self.get_time())

    def test_drop_vowels_all_cases(self):
        self.start_time()
        for sep in self.seps:
            strings = self.CP.parse(self.test_cases, sep=sep, casing='lower', drop_vowels=True)
            for s in strings:
                self.assertNotRegex(s, r'([^a-zA-Z0-9' + sep + '])')
                self.assertRegex(s, r'^[^aeiou]+')
        print(self.get_time())
    
    def test_pascal_case_parse(self):
        self.start_time()
        for sep in self.seps:
            strings = self.CP.parse(self.test_cases, sep=sep, casing='pascal', drop_vowels=False)
            self.assertTrue(word[0].isupper() for word in strings)
            for s in strings:
                self.assertNotRegex(s, r'([^a-zA-Z0-9' + sep + '])')
        print(self.get_time())

    def test_upper_case_parse(self):
        
        for sep in self.seps:
            strings = self.CP.parse(self.test_cases, sep=sep, casing='upper', drop_vowels=False)
            self.assertTrue(word.isupper() for word in strings)
            for s in strings:
                self.assertNotRegex(s, r'([^a-zA-Z0-9' + sep + '])')
        print(self.get_time())

if __name__ == "__main__":
    unittest.main()