/// @file parameters.h
/// @brief defines a struct for the simulation parameters of the Nagel-Schreckenberg model.
#ifndef PARAMETERSH
#define PARAMETERSH

#include <string>

/// @brief struct for the simulation parameters of the Nagel-Schreckenberg model
struct Parameters {
    int    L;     ///< number of positions in the road
    int    T;     ///< total number of time steps
    int    N;     ///< number of cars in the road
    double p;     ///< probability of slowing down
    int    vmax;  ///< maximum velocity
    long   seed;  ///< random number seed
    int    per;   ///< per how mnay steps to write out?
    std::string outputprefix; ///< name of the file to save the data
};

/// @brief Return a set of default parameters
///
/// @return Parameters struct with L=500, T=500, N=300, p=0.2,
///         vmax=2, seed=13, per=1, and outputprefix="trafficMC.txt".
Parameters default_parameters();

/// @brief Read parameters from a file. Missing parameters are set to
///        default values using default_parameters.
///
/// @param  inifilename  file with parameters (in)
///
/// @return Parameters struct
Parameters read_parameters(const std::string& inifilename);

/// @brief Print parameters to console
///
/// @param Parameter struct to print out
///
/// @return void
void print_parameters(const Parameters& params);

#endif

