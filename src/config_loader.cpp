/*
 * Copyright (C) 2011 Red Hat, Inc.
 *
 * Authors: Angus Salkeld <asalkeld@redhat.com>
 *
 * This file is part of pacemaker-cloud.
 *
 * pacemaker-cloud is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * pacemaker-cloud is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with pacemaker-cloud.  If not, see <http://www.gnu.org/licenses/>.
 */
#include <stdlib.h>
#include <qb/qblog.h>

#include "config_loader.h"

int32_t
config_get(std::string& uuid, xmlDoc** doc)
{
	std::string filename = "/var/run/";
	filename +=  uuid + ".xml";

	*doc = xmlParseFile(filename.c_str());
	if (*doc == NULL) {
		qb_log(LOG_ERR, "failed to load %s", filename.c_str());
		return -1;
	}
	qb_log(LOG_INFO, "loaded %s", filename.c_str());
	return 0;
}

