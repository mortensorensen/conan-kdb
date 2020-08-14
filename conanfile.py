from conans import ConanFile, CMake, tools


class KdbConan(ConanFile):
    name = "kdb"
    version = "0.1.0"
    license = "https://github.com/KxSystems/kdb/blob/master/LICENSE"
    url = "https://github.com/mortensorensen/conan-kdb"
    homepage = "https://github.com/KxSystems/kdb"
    description = "Companion files to kdb+ and q"
    topics = ("conan", "kdb", "q", "timeseries")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "tls": [True, False]
    }
    default_options = {
        "shared": True,
        "tls": False
    }
    generators = "cmake"
    exports_sources = "CMakeLists.txt", "kdbConfig.cmake"

    def source(self):
        root_url = "https://raw.githubusercontent.com/KxSystems/kdb/master"
        header = "k.h"
        tools.download("{}/c/c/{}".format(root_url, header), header)

        os = str(self.settings.os)[0].lower()
        arch = "32" if self.settings.arch == "x86" else "64"
        zo = os + arch
        lib_folder = "lib"

        if self.settings.os == "Windows":
            libs = [
                "c.dll",
                "c.lib",
                "cst.dll",
                "cst.lib",
                "c_static.lib",
                "cst_static.lib",
            ]
            if self.settings.tls:
                libs = ['e' + l[1:] for l in libs]

            for lib in libs:
                url = "/".join([root_url, zo, lib])
                tools.download(url, "/".join([lib_folder, lib]))
        else:
            lib = "e" if self.options.tls else "c"
            lib += ".o"
            url = "/".join([root_url, zo, lib])
            tools.download(url, "/".join([lib_folder, lib]))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
