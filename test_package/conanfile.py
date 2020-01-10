from conans import ConanFile, CMake, tools
import os


class KdbTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="lib")
        self.copy("*.lib", dst="bin", src="lib")
        self.copy('*.o', dst="bin", src="lib")

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run(".%sexample" % os.sep)
