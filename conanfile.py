from conans import ConanFile, CMake, tools


class KdbConan(ConanFile):
    name = "kdb"
    version = "1.0.0"
    license = "https://github.com/KxSystems/kdb/blob/master/LICENSE"
    url = "https://github.com/mortensorensen/conan-kdb"
    homepage = "https://github.com/KxSystems/kdb"
    description = "Companion files to kdb+ and q"
    topics = ("conan", "kdb", "q", "timeseries")
    settings = "os", "compiler", "build_type", "arch"
    options = {"tls": [True, False]}
    default_options = {"tls": False}
    generators = "cmake"

    def build(self):
        root_url = "https://raw.githubusercontent.com/KxSystems/kdb/master"
        header = "k.h"
        tools.download("{}/c/c/{}".format(root_url, header), header)
        os_map = {"Linux": "l", "Macos": "m", "Windows": "w", "Solaris": "s"}
        arch_map = {"x86": "32", "x86_64": "64"}
        zo = os_map[str(self.settings.os)] + arch_map[str(self.settings.arch)]
        name = "e" if self.options.tls else "c"

        if self.settings.os == "Windows":
            libs = [
                ".dll",
                ".lib",
                "st.dll",
                "st.lib",
                "_static.lib",
                "st_static.lib",
            ]
            libs = [name + l for l in libs]
            for lib in libs:
                library_url = "{}/{}/{}".format(root_url, zo, lib)
                tools.download(library_url, lib)
        else:
            lib = name + ".o"
            library_url = "{}/{}/{}".format(root_url, zo, lib)
            tools.download(library_url, lib)

    def package(self):
        self.copy("*.h", dst="include/kdb", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.o", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
