# Module-testing package.

import render as render

renderer = render.SetupWindow(pixelWidth=500, pixelHeight=500)
render.DigestRenderQuery(render.makeHelloTriangleRenderQuery(renderer))
renderer[0].mainloop()

