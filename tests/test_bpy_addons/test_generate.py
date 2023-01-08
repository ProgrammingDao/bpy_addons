"""Test cases for object generation."""

import bpy
import numpy.testing as np_testing

from bpy_addons.generate import (
    Circle,
    Cone,
    Cube,
    Cylinder,
    MeshObject,
    Pyramid,
    Sphere,
)


def delete_existing_objects():
    # Delete any existing objects
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)


def create_and_check(mesh: MeshObject):
    delete_existing_objects()
    mesh.create()

    # Check that there is now exactly one object in the scene
    assert len(bpy.data.objects) == 1
    created_mesh = bpy.data.objects[0]

    # Check that the object is a mesh
    assert created_mesh.type == "MESH"
    assert created_mesh.name == type(mesh).__name__
    assert created_mesh.location == mesh.location_vector

    return created_mesh


def test_cube_create():
    cube = Cube((1, 1, 1), 2)
    created_cube = create_and_check(cube)

    np_testing.assert_almost_equal(
        list(created_cube.dimensions), [cube.size for _ in range(3)]
    )


def test_sphere_create():
    sphere = Sphere((1, 1, 1), radius=3)
    created_sphere = create_and_check(sphere)
    np_testing.assert_almost_equal(
        list(created_sphere.dimensions),
        [2 * sphere.radius for _ in range(3)],
        decimal=5,
    )


def test_circle_create():
    circle = Circle((1, 1, 1), radius=3)
    created_disc = create_and_check(circle)
    np_testing.assert_almost_equal(
        list(created_disc.dimensions), [2 * circle.radius, 2 * circle.radius, 0]
    )


def test_cylinder_create():
    cylinder = Cylinder((1, 1, 1), radius=3, depth=1)
    created_cylinder = create_and_check(cylinder)
    np_testing.assert_almost_equal(
        list(created_cylinder.dimensions),
        [2 * cylinder.radius, 2 * cylinder.radius, cylinder.depth],
    )


def test_pyramid_create():
    pyramid = Pyramid((1, 1, 1), size=2)
    created_pyramid = create_and_check(pyramid)
    np_testing.assert_almost_equal(
        list(created_pyramid.dimensions), [pyramid.size for _ in range(3)]
    )


def test_cone_create():
    cone = Cone((1, 1, 1), radius_base=2, depth=3)
    created_cone = create_and_check(cone)
    np_testing.assert_almost_equal(
        list(created_cone.dimensions),
        [2 * cone.radius_base, 2 * cone.radius_base, cone.depth],
    )
