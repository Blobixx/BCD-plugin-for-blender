
# add_subdirectory(bcd)
set(INC
	..
	../../glew-mx
)

set(INC_SYS
	${GLEW_INCLUDE_DIR}
	../../../extern/clew/include
	../../../extern/Eigen3 # for eigen in Bcd.h
)

if(WITH_CUDA_DYNLOAD)
	list(APPEND INC
		../../../extern/cuew/include
	)
	add_definitions(-DWITH_CUDA_DYNLOAD)
else()
	list(APPEND INC_SYS
		${CUDA_TOOLKIT_INCLUDE}
	)
	add_definitions(-DCYCLES_CUDA_NVCC_EXECUTABLE="${CUDA_NVCC_EXECUTABLE}")
endif()

set(SRC
	device.cpp
	device_cpu.cpp
	device_cuda.cpp
	device_denoising.cpp
	device_memory.cpp
	device_multi.cpp
	device_opencl.cpp
	device_split_kernel.cpp
	device_task.cpp
)

set(SRC_OPENCL
	opencl/opencl.h
	opencl/memory_manager.h

	opencl/opencl_base.cpp
	opencl/opencl_mega.cpp
	opencl/opencl_split.cpp
	opencl/opencl_util.cpp
	opencl/memory_manager.cpp
)

SET(SRC_BCD
	../bcd/BayesianCollaborativeDenoiser/Denoiser.cpp
	../bcd/BayesianCollaborativeDenoiser/DenoisingUnit.cpp
	../bcd/BayesianCollaborativeDenoiser/MultiscaleDenoiser.cpp
	../bcd/BayesianCollaborativeDenoiser/SpikeRemovalFilter.cpp
	../bcd/BayesianCollaborativeDenoiser/SamplesAccumulator.cpp
	../bcd/Common/Chronometer.cpp
	../bcd/Common/ImageIO.cpp
	../bcd/Common/Utils.cpp
	../bcd/Common/DeepImage.hpp
	../bcd/Common/CovarianceMatrix.cpp
	../bcd/Common/exr/io_exr.cpp
	../bcd/BayesianCollaborativeDenoiser/CudaHistogramDistance.cu
)

SET(SRC_BCD_HEADERS
	../bcd/BayesianCollaborativeDenoiser/IDenoiser.h
	../bcd/BayesianCollaborativeDenoiser/Denoiser.h
	../bcd/BayesianCollaborativeDenoiser/DenoisingUnit.h
	../bcd/BayesianCollaborativeDenoiser/MultiscaleDenoiser.h
	../bcd/BayesianCollaborativeDenoiser/SpikeRemovalFilter.h
	../bcd/BayesianCollaborativeDenoiser/SamplesAccumulator.h
	../bcd/BayesianCollaborativeDenoiser/Bcd.h
	../bcd/Common/DeepImage.h
	../bcd/Common/Chronometer.h
	../bcd/Common/ImageIO.h
	../bcd/Common/Utils.h
	../bcd/Common/CovarianceMatrix.h
	../bcd/Common/exr/io_exr.h
	../bcd/BayesianCollaborativeDenoiser/CudaHistogramDistance.h
)

if(WITH_CYCLES_NETWORK)
	list(APPEND SRC
		device_network.cpp
	)
endif()

set(SRC_HEADERS
	device.h
	device_denoising.h
	device_memory.h
	device_intern.h
	device_network.h
	device_split_kernel.h
	device_task.h
)

add_definitions(${GL_DEFINITIONS})
if(WITH_CYCLES_NETWORK)
	add_definitions(-DWITH_NETWORK)
endif()
if(WITH_CYCLES_DEVICE_OPENCL)
	add_definitions(-DWITH_OPENCL)
endif()
if(WITH_CYCLES_DEVICE_CUDA)
	add_definitions(-DWITH_CUDA)
endif()
if(WITH_CYCLES_DEVICE_MULTI)
	add_definitions(-DWITH_MULTI)
endif()

include_directories(${INC})
include_directories(SYSTEM ${INC_SYS})

#add_compile_options("-libiomp")
add_compile_options("-fopenmp")
# link_directories("/usr/local/Cellar/llvm/5.0.0/lib")
add_library(cycles_device ${SRC} ${SRC_OPENCL} ${SRC_HEADERS} ${SRC_BCD} ${SRC_BCD_HEADERS})
