# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

import gzip
from io import StringIO, BufferedIOBase #To write the g-code to a temporary buffer, and for typing.
from typing import cast, List

from UM.Logger import Logger
from UM.Mesh.MeshWriter import MeshWriter #The class we're extending/implementing.
from UM.PluginRegistry import PluginRegistry
from UM.Scene.SceneNode import SceneNode #For typing.

##  A file writer that writes gzipped g-code.
#
#   If you're zipping g-code, you might as well use gzip!
class GCodeGzWriter(MeshWriter):
    ##  Writes the gzipped g-code to a stream.
    #
    #   Note that even though the function accepts a collection of nodes, the
    #   entire scene is always written to the file since it is not possible to
    #   separate the g-code for just specific nodes.
    #
    #   \param stream The stream to write the gzipped g-code to.
    #   \param nodes This is ignored.
    #   \param mode Additional information on what type of stream to use. This
    #   must always be binary mode.
    #   \return Whether the write was successful.
    def write(self, stream: BufferedIOBase, nodes: List[SceneNode], mode = MeshWriter.OutputMode.BinaryMode) -> bool:
        if mode != MeshWriter.OutputMode.BinaryMode:
            Logger.log("e", "GCodeGzWriter does not support text mode.")
            return False

        #Get the g-code from the g-code writer.
        gcode_textio = StringIO() #We have to convert the g-code into bytes.
        success = cast(MeshWriter, PluginRegistry.getInstance().getPluginObject("GCodeWriter")).write(gcode_textio, None)
        if not success: #Writing the g-code failed. Then I can also not write the gzipped g-code.
            return False

        result = gzip.compress(gcode_textio.getvalue().encode("utf-8"))
        stream.write(result)
        return True
