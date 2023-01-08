"""Object generation with blender."""

import bpy
from attr import define
from mathutils import Vector


@define(frozen=True)
class MeshObject:
    """Base class for all the mesh objects."""

    location: tuple[float, float, float] = (0, 0, 0)
    """Location in space(x, y, z)."""

    @property
    def location_vector(self) -> Vector:
        """Convert location attribute in vector representation."""
        return Vector(self.location)  # type: ignore[no-untyped-call]

    def create(self) -> None:
        """Create mesh object."""
        raise NotImplementedError


@define(frozen=True)
class SizedObject(MeshObject):
    """Sized Object."""

    size: float = 2.0
    """size."""

    def create(self) -> None:
        """Create mesh object."""
        raise NotImplementedError


@define(frozen=True)
class Cube(SizedObject):
    """Cube."""

    def create(self) -> None:
        """Create cube."""
        bpy.ops.mesh.primitive_cube_add(location=self.location_vector, size=self.size)


@define(frozen=True)
class CircularObject(MeshObject):
    """Circular Object."""

    radius: float = 1.0
    """radius."""
    vertices: int = 32
    """vertices."""

    def create(self) -> None:
        """Create mesh object."""
        raise NotImplementedError


@define(frozen=True)
class Sphere(CircularObject):
    """Sphere."""

    def create(self) -> None:
        """Create sphere."""
        bpy.ops.mesh.primitive_uv_sphere_add(
            location=self.location_vector, radius=self.radius, segments=self.vertices
        )


@define(frozen=True)
class Circle(CircularObject):
    """Disc."""

    def create(self) -> None:
        """Create disc."""
        bpy.ops.mesh.primitive_circle_add(
            location=self.location_vector,
            radius=self.radius,
            vertices=self.vertices,
        )


@define(frozen=True)
class Cylinder(CircularObject):
    """Cylinder."""

    depth: float = 2.0
    """Depth."""

    def create(self) -> None:
        """Create cylinder."""
        bpy.ops.mesh.primitive_cylinder_add(
            location=self.location_vector,
            radius=self.radius,
            depth=self.depth,
            vertices=self.vertices,
        )


@define(frozen=True)
class Cone(MeshObject):
    """Cone."""

    radius_base: float = 1.0
    """radius at the base of the cone."""
    depth: float = 2.0
    """depth."""
    vertices: int = 32
    """vertices."""
    radius_top: float = 0.0
    """radius at the top of the cone."""

    def create(self) -> None:
        """Create cone."""
        bpy.ops.mesh.primitive_cone_add(
            location=self.location_vector,
            radius1=self.radius_base,
            radius2=self.radius_top,
            depth=self.depth,
            vertices=self.vertices,
        )


@define(frozen=True)
class Pyramid(SizedObject):
    """Pyramid."""

    def create(self) -> None:
        """Create pyramid."""
        # Create a cube that will be turned into the pyramid.
        bpy.ops.mesh.primitive_cube_add(location=self.location_vector, size=self.size)

        # Get a reference to the cube
        cube: bpy.types.Object = bpy.context.active_object

        # Rename the cube to be a pyramid
        cube.name = cube.name.replace("Cube", "Pyramid")

        # Get a reference to the cube's mesh data
        mesh: bpy.types.Mesh = cube.data  # type: ignore[assignment]

        # Get a reference to the cube's vertices
        vertices = mesh.vertices

        # Set the z coordinate of the top vertex to 0
        vertices[4].co.z = 0
        vertices[5].co.z = 0
        vertices[6].co.z = 0
        vertices[7].co.z = 0
