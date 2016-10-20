/*===-- serialbox-c/Archive.h -------------------------------------------------------*- C++ -*-===*\
 *
 *                                    S E R I A L B O X
 *
 * This file is distributed under terms of BSD license.
 * See LICENSE.txt for more information
 *
 *===------------------------------------------------------------------------------------------===//
 *
 *! \file
 *! This file contains the C Interface to the ArchiveFactory.
 *
\*===------------------------------------------------------------------------------------------===*/

#ifndef SERIALBOX_C_ARCHIVE_H
#define SERIALBOX_C_ARCHIVE_H

#include "serialbox-c/Array.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \ingroup serialboxC
 * @{
 * 
 * \defgroup archive Archive methods
 * @{
 */

/**
 * \brief Get an array of C-strings of all registered archives
 *
 * The function will allocate a sufficiently large array of `char*`. Each element (as well as the
 * array itself) needs to be freed by the user using free().
 *
 * \return Array of C-strings with the names of all registered archives
 */
serialboxArrayOfString_t* serialboxArchiveGetRegisteredArchives(void);

/** @} @} */

#ifdef __cplusplus
}
#endif

#endif
