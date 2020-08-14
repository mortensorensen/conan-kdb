cmake_minimum_required(VERSION 3.0)

project(kdb C)

set(TARGET_NAME ${PROJECT_NAME})
add_library(${TARGET_NAME} INTERFACE)
# set_target_properties(${TARGET_NAME}
#   PROPERTIES PUBLIC_HEADER "${${TARGET_NAME}_HEADERS}")

set(KDB_LIBRARIES "c.o")

target_include_directories(${TARGET_NAME} INTERFACE
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>"
  "$<INSTALL_INTERFACE:$<INSTALL_PREFIX>/${CMAKE_INSTALL_INCLUDEDIR}>")

#target_link_libraries(${TARGET_NAME} INTERFACE
#  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${CMAKE_INSTALL_LIBDIR}/${KDB_LIBRARIES}>"
#  "$<INSTALL_INTERFACE:$<INSTALL_PREFIX>/${CMAKE_INSTALL_LIBDIR}/${KDB_LIBRARIES}>")

# Write the library and headers
install(
  TARGETS ${TARGET_NAME}
  EXPORT ${TARGET_NAME}Targets
)

# Install header
install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/k.h
  DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/kdb"
)

# Install libraries
install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}/${KDB_LIBRARIES}
  DESTINATION "${CMAKE_INSTALL_LIBDIR}"
)

# Export the target to be used by other projects
export(
  EXPORT ${TARGET_NAME}Targets
  FILE "${CMAKE_CURRENT_BINARY_DIR}/${TARGET_NAME}/${TARGET_NAME}Targets.cmake"
  NAMESPACE ${TARGET_NAME}::
)

set(ConfigPackageLocation lib/cmake/${TARGET_NAME})

# Install the exported target
install(
  EXPORT ${TARGET_NAME}Targets
  FILE ${TARGET_NAME}Targets.cmake
  NAMESPACE ${TARGET_NAME}::
  DESTINATION ${ConfigPackageLocation}
)

# Install the kdbConfig.cmake file
install(
  FILES ${TARGET_NAME}Config.cmake
  DESTINATION ${ConfigPackageLocation}
)
