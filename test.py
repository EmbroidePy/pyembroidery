from __future__ import print_function

import test_fractals
from pyembroidery import *


pattern = EmbPattern()

pattern.add_thread({
    "rgb": 0x0000FF,
    "name": "Blue Test",
    "catalog": "0033",
    "brand": "PyEmbroidery Brand Thread"
})

pattern.add_thread({
    "rgb": 0x00FF00,
    "name": "Green",
    "catalog": "0034",
    "brand": "PyEmbroidery Brand Thread"
})

test_fractals.generate(pattern)

settings = {
    "tie_on": True,
    "tie_off": True
}

write(pattern, "generated.u01", settings)
write(pattern, "generated.pec", settings)
write(pattern, "generated.pes", settings)
write(pattern, "generated.exp", settings)
write(pattern, "generated.dst", settings)
settings["extended header"] = True
write(pattern, "generated-eh.dst", settings)
write(pattern, "generated.jef", settings)
write(pattern, "generated.vp3", settings)
settings["pes version"] = 1,
write(pattern, "generatedv1.pes", settings)
settings["truncated"] = True
write(pattern, "generatedv1t.pes", settings)
settings["pes version"] = 6,
write(pattern, "generatedv6t.pes", settings)

convert("generated.exp", "genconvert.dst", 
        {"stable": False, "encode": False})
