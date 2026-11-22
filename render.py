# Rendering module.
# Nodep.

import tkinter as tk
import typing
import enum

# Color. Must invoke makeColor() to fill in code.
class Color( typing.NamedTuple ) :
    r       : int
    g       : int
    b       : int
    code    : str

# Return x or smaller (inc).
def __max( x : int, y : int ) -> int :
     return y if y <= x else x

# Return x or bigger (inc).
def __min( x : int, y : int ) -> int :
     return y if y >= x else x

# Return between x0 and x1 (inc).
def __minmax( x0 : int, x1 : int, y : int ) -> int :
     return __min( x0, __max( x1, y ) )

# Return between 0 and x (inc)
def __posmax( x : int, y : int ) -> int :
     return __minmax( 0, x, y ) 

# Translate RGB to color code.
def makeColor( r : int, g : int, b : int ) -> Color :
    _r  = __posmax( r, 255 )
    _g  = __posmax( g, 255 )
    _b  = __posmax( b, 255 )
    return Color(
        r       = _r,
        g       = _g,
        b       = _b,
        code    = f"#{_r:02x}{_g:02x}{_b:02x}" )

# Basic rendering information.
class RenderInfoStruct( typing.NamedTuple ) : 
    root        : tk.Tk
    canvas      : tk.Canvas
    pixelWidth  : int
    pixelHeight : int

# Render-Query types.
class RenderQueryT( enum.IntEnum ) :
    line    = 0     # Draw a line.      
    tri2D   = 1     # Draw a 2D triangle.
    tri3D   = 2     # Draw a 3D triangle.

# Type of point. Pixel or relative.
class PointT( enum.IntEnum ) :
    pix    = 0   # Only comprehended for camera-space.
    rel    = 1

# Relativity to camera or world space.
class SpaceT( enum.IntEnum ) :
    camera  = 0
    world   = 1

# A point, consisting of an X, Y and Z component.
class Point( typing.NamedTuple ) :
    type    : PointT
    space   : SpaceT 
    X       : float
    Y       : float
    Z       : float

# Texture-Functor type.
class TexFuncT( enum.IntEnum ):
    constant    = 0     # Constant color.
    UV          = 1     # Callback supplies UV vector.
    UVW         = 2     # Callback supplies UVW vector.

# Texture-Functor.
class TexFunc( typing.NamedTuple ):
    type        : TexFuncT                  # Type.
    callback    : typing.Callable|None      # Callback function. Disregarded when type = 0 (constant)
    color       : Color|None                # Hexadecimal color code. Disregarded when type != 0 (UV/UVW) 

# Render-Query.
class RenderQuery( typing.NamedTuple ): 
    type        : RenderQueryT      # Type of query.
    renderInfo  : RenderInfoStruct  # Rendering info.
    points      : list[Point]       # Points of the shape.
    texture     : TexFunc           # Texture functor.

# Set-up window.
def SetupWindow(
    pixelWidth  : int = 100,
    pixelHeight : int = 100,
    title       : str = "Title",
    bgColor     : str = "#000000" # Hex color code.
    ) -> RenderInfoStruct :
        __root = tk.Tk()
        __root.title(title)
        __canvas = tk.Canvas(   __root,
                                width=pixelWidth,
                                height=pixelHeight,
                                background=bgColor,
                                highlightthickness=0 )
        __canvas.pack()
        return RenderInfoStruct( __root, __canvas, pixelWidth, pixelHeight )

# Raster a wireframe triangle (tri2D).
def __linedraw_tri3d_uv( _p : list[Point], _texfun : TexFunc, _ctx : RenderInfoStruct ) :
    _ctx.canvas.create_line( 
        int( _p[0].X * _ctx.pixelWidth  ),
        int( _p[0].Y * _ctx.pixelHeight ),
        int( _p[1].X * _ctx.pixelWidth  ),
        int( _p[1].Y * _ctx.pixelHeight ),
        width=2,
        fill=_texfun( 0, 0 ).code
    )
    _ctx.canvas.create_line( 
        int( _p[1].X * _ctx.pixelWidth  ),
        int( _p[1].Y * _ctx.pixelHeight ),
        int( _p[2].X * _ctx.pixelWidth  ),
        int( _p[2].Y * _ctx.pixelHeight ),
        width=2,
        fill=_texfun( 1, 0 ).code
    )
    _ctx.canvas.create_line( 
        int( _p[2].X * _ctx.pixelWidth  ),
        int( _p[2].Y * _ctx.pixelHeight ),
        int( _p[0].X * _ctx.pixelWidth  ),
        int( _p[0].Y * _ctx.pixelHeight ),
        width=2,
        fill=_texfun( 0, 1 ).code
    )

# Render queries.
def DigestRenderQuery( query : RenderQuery ):
    if query.type == RenderQueryT.line or query.type == RenderQueryT.tri3D:
        raise NotImplementedError("Only tri2D is implemented.")
    __linedraw_tri3d_uv( query.points, query.texture.callback, query.renderInfo )
      

# Hello Triangle!
def HelloTriangleTexFuncCallback( U : float, V : float ) -> Color :
    return makeColor( int( U * 255 ), int( V * 255 ), int( ( U-V ) * 255 ) )

HelloTriangleTexFunc = TexFunc(
    type=TexFuncT.UV,
    callback=HelloTriangleTexFuncCallback,
    color=None
)

def makeHelloTriangleRenderQuery( renderInfoStruct : RenderInfoStruct ):
    return RenderQuery(
        type=RenderQueryT.tri2D,
        points=[
            Point(
                type=PointT.rel,
                space=SpaceT.camera,
                X=0,
                Y=0,
                Z=0
            ),
            Point(
                type=PointT.rel,
                space=SpaceT.camera,
                X=1,
                Y=0,
                Z=0
            ),
            Point(
                type=PointT.rel,
                space=SpaceT.camera,
                X=0.5,
                Y=1,
                Z=0
            )
        ],
        texture=HelloTriangleTexFunc,
        renderInfo=renderInfoStruct
    )