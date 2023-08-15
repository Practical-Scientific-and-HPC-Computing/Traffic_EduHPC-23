/// @file npywriter.h
/// @brief functions to write to npy files

#ifndef NPYWRITERH
#define NPYWRITERH

#include <string>
#include <fstream>
#include <memory>
#include <vector>

namespace npy {
    
/// @brief struct to hold all info to be able to write to a set of npy files in 'append' mode.
struct Writer {
    std::unique_ptr<std::ofstream> npydens;  ///< variable for density
    std::unique_ptr<std::ofstream> npyvelo;  ///< variable for velocities
    std::unique_ptr<std::ofstream> npytime;  ///< variable for times
    int length;
    int sequencenumber;
    int npydensheadersize; 
    int npyveloheadersize;
    int npytimeheadersize;
};

/// @brief Open a set of npy files for writing positions and velocities
///        on a linear grid.
///
/// @param filename prefix of names of the npy files to be created,
///                 the actual filenames for densities, velocities and
///                 times, will be this prefix appended with
///                 '-dens.npy', '-velo.npy', and '-time.npy', respectively ;
/// @param length   size of the linear grid
///
/// @return npy::Writer struct to be use in subsequent functions from this module
Writer writer_open(std::string filename, int length);

/// @brief Write a grid representation of a time snap shot of car
///        positions and velocities to file.  In the position grid, 0
///        indicates no car, 1 indicates a car.  For the velocities on
///        a grid, the value at a grid point is equal to the velocity
///        of the car on that grid point if there is a car
///        there. Otherwise, it uses the velocity of the first car
///        ahead.
///
/// @param wrtr npy::Writer created with writer_open (in/out)
/// @param t    time index
/// @param x    vector of the positions of the cars
/// @param v    vector of the velocities of the cars
///
/// @return void
void writer_add(Writer& wrtr, int t, const std::vector<int>& x, const std::vector<int>& v);

/// @brief Close the npy files and updated their headers.
///
/// @param wrtr npy::Writer created with writer_open (in/out)
///
/// @return void
void writer_close(Writer& wrtr);

}

#endif

