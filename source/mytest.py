# -*- coding: utf-8 -*-
import sys
import yurlungur as yr

# import yurlungur.tool.util as util
# from yurlungur.core import standalone
# from yurlungur.core import command

# import subprocess
#
# subprocess.call("C:\Program Files\Autodesk\Maya2017\bin\mayapy C:\Users\sumioka-sho\Desktop\Yurlungur\yurlungur")
# subprocess.call("C:\python26\python C:\Users\sumioka-sho\Desktop\Yurlungur\yurlungur --dlg")

# from operator import methodcaller
# from types import MethodType
#
# def nodf(self):
#     return 10
#
# class Obj(object):
#     def __init__(self, value):
#         self._value = value
#
#     def hello(self):
#         print('Hello')
#     # def __getattr__(self, item):
#     #     return getattr(self._value, item)
#
#     def __getattr__(self, item):
#         def _(targ):
#             if targ is None:
#                 return lambda *args, **kwargs: None
#             return lambda *args, **kwargs: methodcaller(item, *args, **kwargs)(targ)
#         return _
#
# def bye():
#     return 2

# class DynamicProxy(object):
#     def __init__(self, value):
#         self._value = value
#
#     def __getattr__(self, item):
#         return getattr(self._value, item)
#
# proc = DynamicProxy("hoge")
# print proc.title()

__doc__ = """
https://docs.python.org\ja\2.7\reference\datamodel.html#customization
https://docs.python.jp\2.7\reference\datamodel.html#object.__new__
"""

# Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.
#

import unreal

obj = unreal.MediaPlayer()

with unreal.ScopedEditorTransaction("FlyingExampleMap") as trans:
    obj.set_editor_property("play_on_open", True)
    obj.set_editor_property("vertical_field_of_view", 60)
    print dir(trans)

# Array < AActor * > Characters;
ue.Array(ue.Actor)

# UGameplayStatics::GetAllActorsOfClass(this, AMyCharacter::StaticClass(), Characters);
print ue.GameplayStatics.get_all_actors_of_class(ue.World().get_world(), ue.StaticMeshActor)

print ue.World(), ue.World().get_world(), ue.World().get_name()
print ue.Level(), ue.Level().get_world(), ue.Level().get_name()

help(ue.Level)
help(ue.GameplayStatics)

print ue.Engine.get_world_from_context_object(ue.World())

print dir(ue.GameplayStatics)

"""
The World is the top level object representing a map or a sandbox in which Actors and Components will exist and be rendered.
 |  A World can be a single Persistent Level with an optional list of streaming levels that are loaded and unloaded via volumes and blueprint functions
 |  or it can be a collection of levels organized with a World Composition.
 |  In a standalone game, generally only a single World exists except during seamless area transitions when both a destination and current world exists.
 |  In the editor many Worlds exist: The level being edited, each PIE instance, each editor tool which has an interactive rendered viewport, and many more.
 |  


class Actor(Object)
 |  Actor is the base class for an Object that can be placed or spawned in a level.
 |  Actors may contain a collection of ActorComponents, which can be used to control how actors move, how they are rendered, etc.
 |  The other main function of an Actor is the replication of properties and function calls across the network during play.
 |  see: https://docs.unrealengine.com/latest/INT/Programming/UnrealArchitecture/Actors/
 |  see: UActorComponent
 |  
 |  ----------------------------------------------------------------------
 |  Editor Properties: (see get_editor_property/set_editor_property)
 |  
 |  allow_tick_before_begin_play
 |      type: bool [Read-Write]
 |      Whether we allow this Actor to tick before it receives the BeginPlay event.
 |      Normally we don't tick actors until after BeginPlay; this setting allows this behavior to be overridden.
 |      This Actor must be able to tick for this setting to be relevant.
 |  
 |  always_relevant
 |      type: bool [Read-Write]
 |      Always relevant for network (overrides bOnlyRelevantToOwner).
 |  
 |  auto_destroy_when_finished
 |      type: bool [Read-Write]
 |      If true then destroy self when "finished", meaning all relevant components report that they are done and no timelines or timers are in flight.
 |  
 |  auto_receive_input
 |      type: AutoReceiveInput [Read-Write]
 |      Automatically registers this actor to receive input from a player.
 |  
 |  block_input
 |      type: bool [Read-Write]
 |      If true, all input on the stack below this actor will not be considered
 |  
 |  can_be_damaged
 |      type: bool [Read-Write]
 |      Whether this actor can take damage. Must be true for damage events (e.g. ReceiveDamage()) to be called.
 |      see: https://www.unrealengine.com/blog/damage-in-ue4
 |      see: TakeDamage(), ReceiveDamage()
 |  
 |  can_be_in_cluster
 |      type: bool [Read-Write]
 |      If true, this actor can be put inside of a GC Cluster to improve Garbage Collection performance
 |  
 |  custom_time_dilation
 |      type: float [Read-Write]
 |      Allow each actor to run at a different time speed. The DeltaTime for a frame is multiplied by the global TimeDilation (in WorldSettings) and this CustomTimeDilation for this actor's tick.
 |  
 |  enable_auto_lod_generation
 |      type: bool [Read-Write]
 |      If true, and if World setting has bEnableHierarchicalLOD equal to true, then it will generate LODActor from groups of clustered Actor
 |  
 |  find_camera_component_when_view_target
 |      type: bool [Read-Write]
 |      If true, this actor should search for an owned camera component to view through when used as a view target.
 |  
 |  generate_overlap_events_during_level_streaming
 |      type: bool [Read-Write]
 |      If true, this actor will generate overlap events when spawned as part of level streaming. You might enable this is in the case where a streaming level loads around an actor and you want overlaps to trigger.
 |  
 |  hidden
 |      type: bool [Read-Write]
 |      Allows us to only see this Actor in the Editor, and not in the actual game.
 |      see: SetActorHiddenInGame()
 |  
 |  ignores_origin_shifting
 |      type: bool [Read-Write]
 |      Whether this actor should not be affected by world origin shifting.
 |  
 |  initial_life_span
 |      type: float [Read-Write]
 |      How long this Actor lives before dying, 0=forever. Note this is the INITIAL value and should not be modified once play has begun.
 |  
 |  input_priority
 |      type: int32 [Read-Write]
 |      The priority of this input component when pushed in to the stack.
 |  
 |  instigator
 |      type: Pawn [Read-Write]
 |      Pawn responsible for damage caused by this actor.
 |  
 |  min_net_update_frequency
 |      type: float [Read-Write]
 |      Used to determine what rate to throttle down to when replicated properties are changing infrequently
 |  
 |  net_cull_distance_squared
 |      type: float [Read-Write]
 |      Square of the max distance from the client's viewpoint that this actor is relevant and will be replicated.
 |  
 |  net_dormancy
 |      type: NetDormancy [Read-Write]
 |      Dormancy setting for actor to take itself off of the replication list without being destroyed on clients.
 |  
 |  net_load_on_client
 |      type: bool [Read-Write]
 |      This actor will be loaded on network clients during map load
 |  
 |  net_priority
 |      type: float [Read-Write]
 |      Priority for this actor when checking for replication in a low bandwidth or saturated situation, higher priority means it is more likely to replicate
 |  
 |  net_update_frequency
 |      type: float [Read-Write]
 |      How often (per second) this actor will be considered for replication, used to determine NetUpdateTime
 |  
 |  net_use_owner_relevancy
 |      type: bool [Read-Write]
 |      If actor has valid Owner, call Owner's IsNetRelevantFor and GetNetPriority
 |  
 |  only_relevant_to_owner
 |      type: bool [Read-Write]
 |      If true, this actor is only relevant to its owner. If this flag is changed during play, all non-owner channels would need to be explicitly closed.
 |  
 |  pivot_offset
 |      type: Vector [Read-Write]
 |      Local space pivot offset for the actor
 |  
 |  primary_actor_tick
 |      type: ActorTickFunction [Read-Write]
 |      Primary Actor tick function, which calls TickActor().
 |      Tick functions can be configured to control whether ticking is enabled, at what time during a frame the update occurs, and to set up tick dependencies.
 |      see: https://docs.unrealengine.com/latest/INT/API/Runtime/Engine/Engine/FTickFunction/
 |      see: AddTickPrerequisiteActor(), AddTickPrerequisiteComponent()
 |  
 |  replicate_movement
 |      type: bool [Read-Write]
 |      If true, replicate movement/location related properties.
 |      Actor must also be set to replicate.
 |      see: SetReplicates()
 |      see: https://docs.unrealengine.com/latest/INT/Gameplay/Networking/Replication/
 |  
 |  replicated_movement
 |      type: RepMovement [Read-Write]
 |      Used for replication of our RootComponent's position and velocity
 |  
 |  replicates
 |      type: bool [Read-Write]
 |      If true, this actor will replicate to remote machines
 |      see: SetReplicates()
 |  
 |  root_component
 |      type: SceneComponent [Read-Write]
 |      Collision primitive that defines the transform (location, rotation, scale) of this Actor.
 |  
 |  spawn_collision_handling_method
 |      type: SpawnActorCollisionHandlingMethod [Read-Write]
 |      Controls how to handle spawning this actor in a situation where it's colliding with something else. "Default" means AlwaysSpawn here.
 |  
 |  sprite_scale
 |      type: float [Read-Write]
 |      The scale to apply to any billboard components in editor builds (happens in any WITH_EDITOR build, including non-cooked games).
 |  
 |  tags
 |      type: Array(Name) [Read-Write]
 |      Array of tags that can be used for grouping and categorizing.
 |  
 |  ----------------------------------------------------------------------
 |  
 |  Method resolution order:
 |      Actor
 |      Object
 |      _ObjectBase
 |      _WrapperBase
 |      object
 |  
 |  Methods defined here:
 |  
 |  actor_has_tag(...)
 |      x.actor_has_tag(tag) -> bool -- See if this actor contains the supplied tag
 |      param: tag (Name)
 |      param: return_value (bool)
 |  
 |  add_actor_local_offset(...)
 |      x.add_actor_local_offset(delta_location, sweep, teleport) -> HitResult -- Adds a delta to the location of this component in its local reference frame.
 |      param: delat_location -- The change in location in local space.
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: delta_location (Vector)
 |      param: sweep_hit_result (HitResult)
 |  
 |  add_actor_local_rotation(...)
 |      x.add_actor_local_rotation(delta_rotation, sweep, teleport) -> HitResult -- Adds a delta to the rotation of this component in its local reference frame
 |      param: delta_rotation (Rotator) -- The change in rotation in local space.
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult)
 |  
 |  add_actor_local_transform(...)
 |      x.add_actor_local_transform(new_transform, sweep, teleport) -> HitResult -- Adds a delta to the transform of this component in its local reference frame
 |      param: new_transform (Transform) -- The change in transform in local space.
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult)
 |  
 |  add_actor_world_offset(...)
 |      x.add_actor_world_offset(delta_location, sweep, teleport) -> HitResult -- Adds a delta to the location of this actor in world space.
 |      param: delta_location (Vector) -- The change in location.
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult) -- The hit result from the move if swept.
 |  
 |  add_actor_world_rotation(...)
 |      x.add_actor_world_rotation(delta_rotation, sweep, teleport) -> HitResult -- Adds a delta to the rotation of this actor in world space.
 |      param: delta_rotation (Rotator) -- The change in rotation.
 |      param: sweep (bool) -- Whether to sweep to the target rotation (not currently supported for rotation).
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult) -- The hit result from the move if swept.
 |  
 |  add_actor_world_transform(...)
 |      x.add_actor_world_transform(delta_transform, sweep, teleport) -> HitResult -- Adds a delta to the transform of this actor in world space. Scale is unchanged.
 |      param: delta_transform (Transform)
 |      param: sweep (bool)
 |      param: sweep_hit_result (HitResult)
 |      param: teleport (bool)
 |  
 |  add_component(...)
 |      x.add_component(template_name, manual_attachment, relative_transform, component_template_context) -> ActorComponent -- Creates a new component and assigns ownership to the Actor this is
 |      called for. Automatic attachment causes the first component created to
 |      become the root, and all subsequent components to be attached under that
 |      root. When bManualAttachment is set, automatic attachment is
 |      skipped and it is up to the user to attach the resulting component (or
 |      set it up as the root) themselves.
 |      see: UK2Node_AddComponent    DO NOT CALL MANUALLY - BLUEPRINT INTERNAL USE ONLY (for Add Component nodes)
 |      param: template_name (Name) -- The name of the Component Template to use.
 |      param: manual_attachment (bool) -- Whether manual or automatic attachment is to be used
 |      param: relative_transform (Transform) -- The relative transform between the new component and its attach parent (automatic only)
 |      param: component_template_context (Object) -- Optional UBlueprintGeneratedClass reference to use to find the template in. If null (or not a BPGC), component is sought in this Actor's class
 |      param: return_value (ActorComponent)
 |  
 |  add_tick_prerequisite_actor(...)
 |      x.add_tick_prerequisite_actor(prerequisite_actor) -- Make this actor tick after PrerequisiteActor. This only applies to this actor's tick function; dependencies for owned components must be set up separately if desired.
 |      param: prerequisite_actor (Actor)
 |  
 |  add_tick_prerequisite_component(...)
 |      x.add_tick_prerequisite_component(prerequisite_component) -- Make this actor tick after PrerequisiteComponent. This only applies to this actor's tick function; dependencies for owned components must be set up separately if desired.
 |      param: prerequisite_component (ActorComponent)
 |  
 |  attach_to_actor(...)
 |      x.attach_to_actor(parent_actor, socket_name, location_rule, rotation_rule, scale_rule, weld_simulated_bodies) -- Attaches the RootComponent of this Actor to the supplied component, optionally at a named socket. It is not valid to call this on components that are not Registered.
 |      param: parent_actor (Actor) -- Actor to attach this actor's RootComponent to
 |      param: socket_name (Name) -- Socket name to attach to, if any
 |      param: location_rule (AttachmentRule) -- How to handle translation when attaching.
 |      param: rotation_rule (AttachmentRule) -- How to handle rotation when attaching.
 |      param: scale_rule (AttachmentRule) -- How to handle scale when attaching.
 |      param: weld_simulated_bodies (bool) -- Whether to weld together simulated physics bodies.
 |  
 |  attach_to_component(...)
 |      x.attach_to_component(parent, socket_name, location_rule, rotation_rule, scale_rule, weld_simulated_bodies) -- Attaches the RootComponent of this Actor to the supplied component, optionally at a named socket. It is not valid to call this on components that are not Registered.
 |      param: parent (SceneComponent) -- Parent to attach to.
 |      param: socket_name (Name) -- Optional socket to attach to on the parent.
 |      param: attachment_rules -- How to handle transforms when attaching.
 |      param: weld_simulated_bodies (bool) -- Whether to weld together simulated physics bodies.
 |      param: location_rule (AttachmentRule)
 |      param: rotation_rule (AttachmentRule)
 |      param: scale_rule (AttachmentRule)
 |  
 |  destroy_actor(...)
 |      x.destroy_actor() -- Destroy the actor
 |  
 |  destroy_component(...)
 |      x.destroy_component(component) -- K2 Destroy Component
 |      param: component (ActorComponent)
 |  
 |  detach_from_actor(...)
 |      x.detach_from_actor(location_rule=KeepRelative, rotation_rule=KeepRelative, scale_rule=KeepRelative) -- Detaches the RootComponent of this Actor from any SceneComponent it is currently attached to.
 |      param: location_rule (DetachmentRule) -- How to handle translation when detaching.
 |      param: rotation_rule (DetachmentRule) -- How to handle rotation when detaching.
 |      param: scale_rule (DetachmentRule) -- How to handle scale when detaching.
 |  
 |  disable_input(...)
 |      x.disable_input(player_controller) -- Removes this actor from the stack of input being handled by a PlayerController.
 |      param: player_controller (PlayerController) -- The PlayerController whose input events we no longer want to receive. If null, this actor will stop receiving input from all PlayerControllers.
 |  
 |  enable_input(...)
 |      x.enable_input(player_controller) -- Pushes this actor on to the stack of input being handled by a PlayerController.
 |      param: player_controller (PlayerController) -- The PlayerController whose input events we want to receive.
 |  
 |  flush_net_dormancy(...)
 |      x.flush_net_dormancy() -- Forces dormant actor to replicate but doesn't change NetDormancy state (i.e., they will go dormant again if left dormant)
 |  
 |  force_net_update(...)
 |      x.force_net_update() -- Force actor to be updated to clients
 |  
 |  get_actor_bounds(...)
 |      x.get_actor_bounds(only_colliding_components) -> (Vector, box_extent=Vector) -- Returns the bounding box of all components that make up this Actor (excluding ChildActorComponents).
 |      param: only_colliding_components (bool) -- If true, will only return the bounding box for components with collision enabled.
 |      param: origin (Vector)
 |      param: box_extent (Vector)
 |  
 |  get_actor_enable_collision(...)
 |      x.get_actor_enable_collision() -> bool -- Get current state of collision for the whole actor
 |      param: return_value (bool)
 |  
 |  get_actor_eyes_view_point(...)
 |      x.get_actor_eyes_view_point() -> (Vector, rotation=Rotator) -- Returns the point of view of the actor.
 |      Note that this doesn't mean the camera, but the 'eyes' of the actor.
 |      For example, for a Pawn, this would define the eye height location,
 |      and view rotation (which is different from the pawn rotation which has a zeroed pitch component).
 |      A camera first person view will typically use this view point. Most traces (weapon, AI) will be done from this view point.
 |      param: location (Vector) -- location of view point
 |      param: rotation (Rotator) -- view rotation of actor.
 |  
 |  get_actor_forward_vector(...)
 |      x.get_actor_forward_vector() -> Vector -- Get the forward (X) vector (length 1.0) from this Actor, in world space.
 |      param: return_value (Vector)
 |  
 |  get_actor_label(...)
 |      x.get_actor_label() -> String -- Returns this actor's current label.  Actor labels are only available in development builds.
 |      param: return_value (String)
 |      return: The label text
 |  
 |  get_actor_location(...)
 |      x.get_actor_location() -> Vector -- Returns the location of the RootComponent of this Actor
 |      param: return_value (Vector)
 |  
 |  get_actor_relative_scale3d(...)
 |      x.get_actor_relative_scale3d() -> Vector -- Return the actor's relative scale 3d
 |      param: return_value (Vector)
 |  
 |  get_actor_right_vector(...)
 |      x.get_actor_right_vector() -> Vector -- Get the right (Y) vector (length 1.0) from this Actor, in world space.
 |      param: return_value (Vector)
 |  
 |  get_actor_rotation(...)
 |      x.get_actor_rotation() -> Rotator -- Returns rotation of the RootComponent of this Actor.
 |      param: return_value (Rotator)
 |  
 |  get_actor_scale3d(...)
 |      x.get_actor_scale3d() -> Vector -- Returns the Actor's world-space scale.
 |      param: return_value (Vector)
 |  
 |  get_actor_tick_interval(...)
 |      x.get_actor_tick_interval() -> float -- Returns the tick interval of this actor's primary tick function
 |      param: return_value (float)
 |  
 |  get_actor_time_dilation(...)
 |      x.get_actor_time_dilation() -> float -- Get CustomTimeDilation - this can be used for input control or speed control for slomo.
 |      We don't want to scale input globally because input can be used for UI, which do not care for TimeDilation.
 |      param: return_value (float)
 |  
 |  get_actor_transform(...)
 |      x.get_actor_transform() -> Transform -- Get the actor-to-world transform.
 |      param: return_value (Transform)
 |      return: The transform that transforms from actor space to world space.
 |  
 |  get_actor_up_vector(...)
 |      x.get_actor_up_vector() -> Vector -- Get the up (Z) vector (length 1.0) from this Actor, in world space.
 |      param: return_value (Vector)
 |  
 |  get_all_child_actors(...)
 |      x.get_all_child_actors(include_descendants=true) -> Array(Actor) -- Returns a list of all child actors, including children of children
 |      param: child_actors (Array(Actor))
 |      param: include_descendants (bool)
 |  
 |  get_attach_parent_actor(...)
 |      x.get_attach_parent_actor() -> Actor -- Walk up the attachment chain from RootComponent until we encounter a different actor, and return it. If we are not attached to a component in a different actor, returns nullptr
 |      param: return_value (Actor)
 |  
 |  get_attach_parent_socket_name(...)
 |      x.get_attach_parent_socket_name() -> Name -- Walk up the attachment chain from RootComponent until we encounter a different actor, and return the socket name in the component. If we are not attached to a component in a different actor, returns NAME_None
 |      param: return_value (Name)
 |  
 |  get_attached_actors(...)
 |      x.get_attached_actors() -> Array(Actor) -- Find all Actors which are attached directly to a component in this actor
 |      param: actors (Array(Actor))
 |  
 |  get_component_by_class(...)
 |      x.get_component_by_class(component_class) -> ActorComponent -- Script exposed version of FindComponentByClass
 |      param: component_class (type(Class))
 |      param: return_value (ActorComponent)
 |  
 |  get_components_by_class(...)
 |      x.get_components_by_class(component_class) -> Array(ActorComponent) -- Gets all the components that inherit from the given class.
 |      Currently returns an array of UActorComponent which must be cast to the correct type.
 |      param: component_class (type(Class))
 |      param: return_value (Array(ActorComponent))
 |  
 |  get_components_by_tag(...)
 |      x.get_components_by_tag(component_class, tag) -> Array(ActorComponent) -- Gets all the components that inherit from the given class with a given tag.
 |      param: component_class (type(Class))
 |      param: tag (Name)
 |      param: return_value (Array(ActorComponent))
 |  
 |  get_distance_to(...)
 |      x.get_distance_to(other_actor) -> float -- Returns the distance from this Actor to OtherActor.
 |      param: other_actor (Actor)
 |      param: return_value (float)
 |  
 |  get_dot_product_to(...)
 |      x.get_dot_product_to(other_actor) -> float -- Returns the dot product from this Actor to OtherActor. Returns -2.0 on failure. Returns 0.0 for coincidental actors.
 |      param: other_actor (Actor)
 |      param: return_value (float)
 |  
 |  get_folder_path(...)
 |      x.get_folder_path() -> Name -- Returns this actor's folder path. Actor folder paths are only available in development builds.
 |      param: return_value (Name)
 |      return: The folder path
 |  
 |  get_game_time_since_creation(...)
 |      x.get_game_time_since_creation() -> float -- The number of seconds (in game time) since this Actor was created, relative to Get Game Time In Seconds.
 |      param: return_value (float)
 |  
 |  get_horizontal_distance_to(...)
 |      x.get_horizontal_distance_to(other_actor) -> float -- Returns the distance from this Actor to OtherActor, ignoring Z.
 |      param: other_actor (Actor)
 |      param: return_value (float)
 |  
 |  get_horizontal_dot_product_to(...)
 |      x.get_horizontal_dot_product_to(other_actor) -> float -- Returns the dot product from this Actor to OtherActor, ignoring Z. Returns -2.0 on failure. Returns 0.0 for coincidental actors.
 |      param: other_actor (Actor)
 |      param: return_value (float)
 |  
 |  get_input_axis_key_value(...)
 |      x.get_input_axis_key_value(input_axis_key) -> float -- Gets the value of the input axis key if input is enabled for this actor.
 |      param: input_axis_key (Key)
 |      param: return_value (float)
 |  
 |  get_input_axis_value(...)
 |      x.get_input_axis_value(input_axis_name) -> float -- Gets the value of the input axis if input is enabled for this actor.
 |      param: input_axis_name (Name)
 |      param: return_value (float)
 |  
 |  get_input_vector_axis_value(...)
 |      x.get_input_vector_axis_value(input_axis_key) -> Vector -- Gets the value of the input axis key if input is enabled for this actor.
 |      param: input_axis_key (Key)
 |      param: return_value (Vector)
 |  
 |  get_instigator(...)
 |      x.get_instigator() -> Pawn -- Returns the instigator for this actor, or nullptr if there is none.
 |      param: return_value (Pawn)
 |  
 |  get_instigator_controller(...)
 |      x.get_instigator_controller() -> Controller -- Returns the instigator's controller for this actor, or nullptr if there is none.
 |      param: return_value (Controller)
 |  
 |  get_life_span(...)
 |      x.get_life_span() -> float -- Get the remaining lifespan of this actor. If zero is returned the actor lives forever.
 |      param: return_value (float)
 |  
 |  get_overlapping_actors(...)
 |      x.get_overlapping_actors(class_filter) -> Array(Actor) -- Returns list of actors this actor is overlapping (any component overlapping any component). Does not return itself.
 |      param: overlapping_actors (Array(Actor)) -- [out] Returned list of overlapping actors
 |      param: class_filter (type(Class)) -- [optional] If set, only returns actors of this class or subclasses
 |  
 |  get_overlapping_components(...)
 |      x.get_overlapping_components() -> Array(PrimitiveComponent) -- Returns list of components this actor is overlapping.
 |      param: overlapping_components (Array(PrimitiveComponent))
 |  
 |  get_owner(...)
 |      x.get_owner() -> Actor -- Get the owner of this Actor, used primarily for network replication.
 |      param: return_value (Actor)
 |      return: Actor that owns this Actor
 |  
 |  get_parent_actor(...)
 |      x.get_parent_actor() -> Actor -- If this Actor was created by a Child Actor Component returns the Actor that owns that Child Actor Component
 |      param: return_value (Actor)
 |  
 |  get_parent_component(...)
 |      x.get_parent_component() -> ChildActorComponent -- If this Actor was created by a Child Actor Component returns that Child Actor Component
 |      param: return_value (ChildActorComponent)
 |  
 |  get_remote_role(...)
 |      x.get_remote_role() -> NetRole -- Returns how much control the remote machine has over this actor.
 |      param: return_value (NetRole)
 |  
 |  get_squared_distance_to(...)
 |      x.get_squared_distance_to(other_actor) -> float -- Returns the squared distance from this Actor to OtherActor.
 |      param: other_actor (Actor)
 |      param: return_value (float)
 |  
 |  get_tickable_when_paused(...)
 |      x.get_tickable_when_paused() -> bool -- Gets whether this actor can tick when paused.
 |      param: return_value (bool)
 |  
 |  get_velocity(...)
 |      x.get_velocity() -> Vector -- Returns velocity (in cm/s (Unreal Units/second) of the rootcomponent if it is either using physics or has an associated MovementComponent
 |      param: return_value (Vector)
 |  
 |  get_vertical_distance_to(...)
 |      x.get_vertical_distance_to(other_actor) -> float -- Returns the distance from this Actor to OtherActor, ignoring XY.
 |      param: other_actor (Actor)
 |      param: return_value (float)
 |  
 |  has_authority(...)
 |      x.has_authority() -> bool -- Returns whether this actor has network authority
 |      param: return_value (bool)
 |  
 |  is_actor_being_destroyed(...)
 |      x.is_actor_being_destroyed() -> bool -- Is Actor Being Destroyed
 |      param: return_value (bool)
 |  
 |  is_actor_tick_enabled(...)
 |      x.is_actor_tick_enabled() -> bool -- Returns whether this actor has tick enabled or not
 |      param: return_value (bool)
 |  
 |  is_child_actor(...)
 |      x.is_child_actor() -> bool -- Returns whether this Actor was spawned by a child actor component
 |      param: return_value (bool)
 |  
 |  is_editable(...)
 |      x.is_editable() -> bool -- 
 |      param: return_value (bool)
 |      return: Returns true if this actor is allowed to be displayed, selected and manipulated by the editor.
 |  
 |  is_hidden_ed(...)
 |      x.is_hidden_ed() -> bool -- Returns true if this actor is hidden in the editor viewports.
 |      param: return_value (bool)
 |  
 |  is_hidden_ed_at_startup(...)
 |      x.is_hidden_ed_at_startup() -> bool -- Simple accessor to check if the actor is hidden upon editor startup
 |      param: return_value (bool)
 |      return: true if the actor is hidden upon editor startup; false if it is not
 |  
 |  is_overlapping_actor(...)
 |      x.is_overlapping_actor(other) -> bool -- Check whether any component of this Actor is overlapping any component of another Actor.
 |      param: other (Actor) -- The other Actor to test against
 |      param: return_value (bool)
 |      return: Whether any component of this Actor is overlapping any component of another Actor.
 |  
 |  is_selectable(...)
 |      x.is_selectable() -> bool -- 
 |      param: return_value (bool)
 |      return: Returns true if this actor can EVER be selected in a level in the editor.  Can be overridden by specific actors to make them unselectable.
 |  
 |  is_temporarily_hidden_in_editor(...)
 |      x.is_temporarily_hidden_in_editor(include_parent=false) -> bool -- 
 |      param: include_parent (bool) -- Whether to recurse up child actor hierarchy or not
 |      param: return_value (bool)
 |      return: Whether or not this actor is hidden in the editor for the duration of the current editor session
 |  
 |  make_mid_for_material(...)
 |      x.make_mid_for_material(parent) -> MaterialInstanceDynamic -- Make MIDFor Material
 |      param: parent (MaterialInterface)
 |      param: return_value (MaterialInstanceDynamic)
 |  
 |  make_noise(...)
 |      x.make_noise(loudness=1.000000, noise_instigator, noise_location, max_range=0.000000, tag=None) -- Trigger a noise caused by a given Pawn, at a given location.
 |      Note that the NoiseInstigator Pawn MUST have a PawnNoiseEmitterComponent for the noise to be detected by a PawnSensingComponent.
 |      Senders of MakeNoise should have an Instigator if they are not pawns, or pass a NoiseInstigator.
 |      param: loudness (float) -- The relative loudness of this noise. Usual range is 0 (no noise) to 1 (full volume). If MaxRange is used, this scales the max range, otherwise it affects the hearing range specified by the sensor.
 |      param: noise_instigator (Pawn) -- Pawn responsible for this noise.  Uses the actor's Instigator if NoiseInstigator is null
 |      param: noise_location (Vector) -- Position of noise source.  If zero vector, use the actor's location.
 |      param: max_range (float) -- Max range at which the sound may be heard. A value of 0 indicates no max range (though perception may have its own range). Loudness scales the range. (Note: not supported for legacy PawnSensingComponent, only for AIPerception)
 |      param: tag (Name) -- Identifier for the noise.
 |  
 |  on_become_view_target(...)
 |      x.on_become_view_target(pc) -- Event called when this Actor becomes the view target for the given PlayerController.
 |      param: pc (PlayerController)
 |  
 |  on_end_view_target(...)
 |      x.on_end_view_target(pc) -- Event called when this Actor is no longer the view target for the given PlayerController.
 |      param: pc (PlayerController)
 |  
 |  on_reset(...)
 |      x.on_reset() -- Event called when this Actor is reset to its initial state - used when restarting level without reloading.
 |  
 |  prestream_textures(...)
 |      x.prestream_textures(seconds, enable_streaming, cinematic_texture_groups=0) -- Calls PrestreamTextures() for all the actor's meshcomponents.
 |      param: seconds (float) -- Number of seconds to force all mip-levels to be resident
 |      param: enable_streaming (bool) -- Whether to start (true) or stop (false) streaming
 |      param: cinematic_texture_groups (int32) -- Bitfield indicating which texture groups that use extra high-resolution mips
 |  
 |  receive_actor_begin_cursor_over(...)
 |      x.receive_actor_begin_cursor_over() -- Event when this actor has the mouse moved over it with the clickable interface.
 |  
 |  receive_actor_begin_overlap(...)
 |      x.receive_actor_begin_overlap(other_actor) -- Event when this actor overlaps another actor, for example a player walking into a trigger.
 |      For events when objects have a blocking collision, for example a player hitting a wall, see 'Hit' events.
 |      note: Components on both this and the other Actor must have bGenerateOverlapEvents set to true to generate overlap events.
 |      param: other_actor (Actor)
 |  
 |  receive_actor_end_cursor_over(...)
 |      x.receive_actor_end_cursor_over() -- Event when this actor has the mouse moved off of it with the clickable interface.
 |  
 |  receive_actor_end_overlap(...)
 |      x.receive_actor_end_overlap(other_actor) -- Event when an actor no longer overlaps another actor, and they have separated.
 |      note: Components on both this and the other Actor must have bGenerateOverlapEvents set to true to generate overlap events.
 |      param: other_actor (Actor)
 |  
 |  receive_actor_on_clicked(...)
 |      x.receive_actor_on_clicked(button_pressed) -- Event when this actor is clicked by the mouse when using the clickable interface.
 |      param: button_pressed (Key)
 |  
 |  receive_actor_on_input_touch_begin(...)
 |      x.receive_actor_on_input_touch_begin(finger_index) -- Event when this actor is touched when click events are enabled.
 |      param: finger_index (TouchIndex)
 |  
 |  receive_actor_on_input_touch_end(...)
 |      x.receive_actor_on_input_touch_end(finger_index) -- Event when this actor is under the finger when untouched when click events are enabled.
 |      param: finger_index (TouchIndex)
 |  
 |  receive_actor_on_input_touch_enter(...)
 |      x.receive_actor_on_input_touch_enter(finger_index) -- Event when this actor has a finger moved over it with the clickable interface.
 |      param: finger_index (TouchIndex)
 |  
 |  receive_actor_on_input_touch_leave(...)
 |      x.receive_actor_on_input_touch_leave(finger_index) -- Event when this actor has a finger moved off of it with the clickable interface.
 |      param: finger_index (TouchIndex)
 |  
 |  receive_actor_on_released(...)
 |      x.receive_actor_on_released(button_released) -- Event when this actor is under the mouse when left mouse button is released while using the clickable interface.
 |      param: button_released (Key)
 |  
 |  receive_any_damage(...)
 |      x.receive_any_damage(damage, damage_type, instigated_by, damage_causer) -- Event when this actor takes ANY damage
 |      param: damage (float)
 |      param: damage_type (DamageType)
 |      param: instigated_by (Controller)
 |      param: damage_causer (Actor)
 |  
 |  receive_begin_play(...)
 |      x.receive_begin_play() -- Event when play begins for this actor.
 |  
 |  receive_destroyed(...)
 |      x.receive_destroyed() -- Receive Destroyed
 |  
 |  receive_end_play(...)
 |      x.receive_end_play(end_play_reason) -- Event to notify blueprints this actor is about to be deleted.
 |      param: end_play_reason (EndPlayReason)
 |  
 |  receive_hit(...)
 |      x.receive_hit(my_comp, other, other_comp, self_moved, hit_location, hit_normal, normal_impulse, hit) -- Event when this actor bumps into a blocking object, or blocks another actor that bumps into it.
 |      This could happen due to things like Character movement, using Set Location with 'sweep' enabled, or physics simulation.
 |      For events when objects overlap (e.g. walking into a trigger) see the 'Overlap' event.
 |      note: For collisions during physics simulation to generate hit events, 'Simulation Generates Hit Events' must be enabled.
 |      note: When receiving a hit from another object's movement (bSelfMoved is false), the directions of 'Hit.Normal' and 'Hit.ImpactNormal' will be adjusted to indicate force from the other object against this object.
 |      note: NormalImpulse will be filled in for physics-simulating bodies, but will be zero for swept-component blocking collisions.
 |      param: my_comp (PrimitiveComponent)
 |      param: other (Actor)
 |      param: other_comp (PrimitiveComponent)
 |      param: self_moved (bool)
 |      param: hit_location (Vector)
 |      param: hit_normal (Vector)
 |      param: normal_impulse (Vector)
 |      param: hit (HitResult)
 |  
 |  receive_point_damage(...)
 |      x.receive_point_damage(damage, damage_type, hit_location, hit_normal, hit_component, bone_name, shot_from_direction, instigated_by, damage_causer, hit_info) -- Event when this actor takes POINT damage
 |      param: damage (float)
 |      param: damage_type (DamageType)
 |      param: hit_location (Vector)
 |      param: hit_normal (Vector)
 |      param: hit_component (PrimitiveComponent)
 |      param: bone_name (Name)
 |      param: shot_from_direction (Vector)
 |      param: instigated_by (Controller)
 |      param: damage_causer (Actor)
 |      param: hit_info (HitResult)
 |  
 |  receive_radial_damage(...)
 |      x.receive_radial_damage(damage_received, damage_type, origin, hit_info, instigated_by, damage_causer) -- Event when this actor takes RADIAL damage
 |      todo: Pass it the full array of hits instead of just one?
 |      param: damage_received (float)
 |      param: damage_type (DamageType)
 |      param: origin (Vector)
 |      param: hit_info (HitResult)
 |      param: instigated_by (Controller)
 |      param: damage_causer (Actor)
 |  
 |  receive_tick(...)
 |      x.receive_tick(delta_seconds) -- Event called every frame
 |      param: delta_seconds (float)
 |  
 |  remove_tick_prerequisite_actor(...)
 |      x.remove_tick_prerequisite_actor(prerequisite_actor) -- Remove tick dependency on PrerequisiteActor.
 |      param: prerequisite_actor (Actor)
 |  
 |  remove_tick_prerequisite_component(...)
 |      x.remove_tick_prerequisite_component(prerequisite_component) -- Remove tick dependency on PrerequisiteComponent.
 |      param: prerequisite_component (ActorComponent)
 |  
 |  set_actor_enable_collision(...)
 |      x.set_actor_enable_collision(new_actor_enable_collision) -- Allows enabling/disabling collision for the whole actor
 |      param: new_actor_enable_collision (bool)
 |  
 |  set_actor_hidden_in_game(...)
 |      x.set_actor_hidden_in_game(new_hidden) -- Sets the actor to be hidden in the game
 |      param: new_hidden (bool) -- Whether or not to hide the actor and all its components
 |  
 |  set_actor_label(...)
 |      x.set_actor_label(new_actor_label, mark_dirty=true) -- Assigns a new label to this actor.  Actor labels are only available in development builds.
 |      param: new_actor_label (String) -- The new label string to assign to the actor.  If empty, the actor will have a default label.
 |      param: mark_dirty (bool) -- If true the actor's package will be marked dirty for saving.  Otherwise it will not be.  You should pass false for this parameter if dirtying is not allowed (like during loads)
 |  
 |  set_actor_location(...)
 |      x.set_actor_location(new_location, sweep, teleport) -> HitResult or None -- Move the Actor to the specified location.
 |      param: new_location (Vector) -- The new location to move the Actor to.
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult) -- The hit result from the move if swept.
 |      param: return_value (bool)
 |      return: Whether the location was successfully set (if not swept), or whether movement occurred at all (if swept).
 |  
 |  set_actor_location_and_rotation(...)
 |      x.set_actor_location_and_rotation(new_location, new_rotation, sweep, teleport) -> HitResult or None -- Move the actor instantly to the specified location and rotation.
 |      param: new_location (Vector) -- The new location to teleport the Actor to.
 |      param: new_rotation (Rotator) -- The new rotation for the Actor.
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult) -- The hit result from the move if swept.
 |      param: return_value (bool)
 |      return: Whether the rotation was successfully set.
 |  
 |  set_actor_relative_location(...)
 |      x.set_actor_relative_location(new_relative_location, sweep, teleport) -> HitResult -- Set the actor's RootComponent to the specified relative location.
 |      param: new_relative_location (Vector) -- New relative location of the actor's root component
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult)
 |  
 |  set_actor_relative_rotation(...)
 |      x.set_actor_relative_rotation(new_relative_rotation, sweep, teleport) -> HitResult -- Set the actor's RootComponent to the specified relative rotation
 |      param: new_relative_rotation (Rotator) -- New relative rotation of the actor's root component
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult)
 |  
 |  set_actor_relative_scale3d(...)
 |      x.set_actor_relative_scale3d(new_relative_scale) -- Set the actor's RootComponent to the specified relative scale 3d
 |      param: new_relative_scale (Vector) -- New scale to set the actor's RootComponent to
 |  
 |  set_actor_relative_transform(...)
 |      x.set_actor_relative_transform(new_relative_transform, sweep, teleport) -> HitResult -- Set the actor's RootComponent to the specified relative transform
 |      param: new_relative_transform (Transform) -- New relative transform of the actor's root component
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult)
 |  
 |  set_actor_rotation(...)
 |      x.set_actor_rotation(new_rotation, teleport_physics) -> bool -- Set the Actor's rotation instantly to the specified rotation.
 |      param: new_rotation (Rotator) -- The new rotation for the Actor.
 |      param: teleport_physics (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts).
 |      param: return_value (bool)
 |      return: Whether the rotation was successfully set.
 |  
 |  set_actor_scale3d(...)
 |      x.set_actor_scale3d(new_scale3d) -- Set the Actor's world-space scale.
 |      param: new_scale3d (Vector)
 |  
 |  set_actor_tick_enabled(...)
 |      x.set_actor_tick_enabled(enabled) -- Set this actor's tick functions to be enabled or disabled. Only has an effect if the function is registered
 |      This only modifies the tick function on actor itself
 |      param: enabled (bool) -- Whether it should be enabled or not
 |  
 |  set_actor_tick_interval(...)
 |      x.set_actor_tick_interval(tick_interval) -- Sets the tick interval of this actor's primary tick function. Will not enable a disabled tick function. Takes effect on next tick.
 |      param: tick_interval (float) -- The rate at which this actor should be ticking
 |  
 |  set_actor_transform(...)
 |      x.set_actor_transform(new_transform, sweep, teleport) -> HitResult or None -- Set the Actors transform to the specified one.
 |      param: new_transform (Transform) -- The new transform.
 |      param: sweep (bool) -- Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
 |      param: teleport (bool) -- Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not telep
orting, this will affect objects along the entire swept volume.
 |      param: sweep_hit_result (HitResult)
 |      param: return_value (bool)
 |  
 |  set_folder_path(...)
 |      x.set_folder_path(new_folder_path) -- Assigns a new folder to this actor. Actor folder paths are only available in development builds.
 |      param: new_folder_path (Name) -- The new folder to assign to the actor.
 |  
 |  set_is_temporarily_hidden_in_editor(...)
 |      x.set_is_temporarily_hidden_in_editor(is_hidden) -- Sets whether or not this actor is hidden in the editor for the duration of the current editor session
 |      param: is_hidden (bool) -- True if the actor is hidden
 |  
 |  set_life_span(...)
 |      x.set_life_span(lifespan) -- Set the lifespan of this actor. When it expires the object will be destroyed. If requested lifespan is 0, the timer is cleared and the actor will not be destroyed.
 |      param: lifespan (float)
 |  
 |  set_net_dormancy(...)
 |      x.set_net_dormancy(new_dormancy) -- Puts actor in dormant networking state
 |      param: new_dormancy (NetDormancy)
 |  
 |  set_owner(...)
 |      x.set_owner(new_owner) -- Set the owner of this Actor, used primarily for network replication.
 |      param: new_owner (Actor) -- The Actor whom takes over ownership of this Actor
 |  
 |  set_replicate_movement(...)
 |      x.set_replicate_movement(replicate_movement) -- Set whether this actor's movement replicates to network clients.
 |      param: replicate_movement (bool) -- Whether this Actor's movement replicates to clients.
 |  
 |  set_replicates(...)
 |      x.set_replicates(replicates) -- Set whether this actor replicates to network clients. When this actor is spawned on the server it will be sent to clients as well.
 |      Properties flagged for replication will update on clients if they change on the server.
 |      Internally changes the RemoteRole property and handles the cases where the actor needs to be added to the network actor list.
 |      see: https://docs.unrealengine.com/latest/INT/Gameplay/Networking/Replication/
 |      param: replicates (bool) -- Whether this Actor replicates to network clients.
 |  
 |  set_tick_group(...)
 |      x.set_tick_group(new_tick_group) -- Sets the ticking group for this actor.
 |      param: new_tick_group (TickingGroup) -- the new value to assign
 |  
 |  set_tickable_when_paused(...)
 |      x.set_tickable_when_paused(tickable_when_paused) -- Sets whether this actor can tick when paused.
 |      param: tickable_when_paused (bool)
 |  
 |  tear_off(...)
 |      x.tear_off() -- Networking - Server - TearOff this actor to stop replication to clients. Will set bTearOff to true.
 |  
 |  teleport(...)
 |      x.teleport(dest_location, dest_rotation) -> bool -- Teleport this actor to a new location. If the actor doesn't fit exactly at the location specified, tries to slightly move it out of walls and such.
 |      param: dest_location (Vector) -- The target destination point
 |      param: dest_rotation (Rotator) -- The target rotation at the destination
 |      param: return_value (bool)
 |      return: true if the actor has been successfully moved, or false if it couldn't fit.
 |  
 |  user_construction_script(...)
 |      x.user_construction_script() -- Construction script, the place to spawn components and do other setup.
 |      note: Name used in CreateBlueprint function
 |      param: location -- The location.
 |      param: rotation -- The rotation.
 |  
 |  was_recently_rendered(...)
 |      x.was_recently_rendered(tolerance=0.200000) -> bool -- Returns true if this actor has been rendered "recently", with a tolerance in seconds to define what "recent" means.
 |      e.g.: If a tolerance of 0.1 is used, this function will return true only if the actor was rendered in the last 0.1 seconds of game time.
 |      param: tolerance (float) -- How many seconds ago the actor last render time can be and still count as having been "recently" rendered.
 |      param: return_value (bool)
 |      return: Whether this actor was recently rendered.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  always_relevant
 |      type: bool [Read-Write]
 |      Always relevant for network (overrides bOnlyRelevantToOwner).
 |  
 |  auto_destroy_when_finished
 |      type: bool [Read-Write]
 |      If true then destroy self when "finished", meaning all relevant components report that they are done and no timelines or timers are in flight.
 |  
 |  can_be_damaged
 |      type: bool [Read-Write]
 |      Whether this actor can take damage. Must be true for damage events (e.g. ReceiveDamage()) to be called.
 |      see: https://www.unrealengine.com/blog/damage-in-ue4
 |      see: TakeDamage(), ReceiveDamage()
 |  
 |  custom_time_dilation
 |      type: float [Read-Write]
 |      Allow each actor to run at a different time speed. The DeltaTime for a frame is multiplied by the global TimeDilation (in WorldSettings) and this CustomTimeDilation for this actor's tick.
 |  
 |  find_camera_component_when_view_target
 |      type: bool [Read-Write]
 |      If true, this actor should search for an owned camera component to view through when used as a view target.
 |  
 |  generate_overlap_events_during_level_streaming
 |      type: bool [Read-Write]
 |      If true, this actor will generate overlap events when spawned as part of level streaming. You might enable this is in the case where a streaming level loads around an actor and you want overlaps to trigger.
 |  
 |  hidden
 |      type: bool [Read-Only]
 |      Allows us to only see this Actor in the Editor, and not in the actual game.
 |      see: SetActorHiddenInGame()
 |  
 |  initial_life_span
 |      type: float [Read-Only]
 |      How long this Actor lives before dying, 0=forever. Note this is the INITIAL value and should not be modified once play has begun.
 |  
 |  instigator
 |      type: Pawn [Read-Write]
 |      Pawn responsible for damage caused by this actor.
 |  
 |  min_net_update_frequency
 |      type: float [Read-Write]
 |      Used to determine what rate to throttle down to when replicated properties are changing infrequently
 |  
 |  net_cull_distance_squared
 |      type: float [Read-Only]
 |      Square of the max distance from the client's viewpoint that this actor is relevant and will be replicated.
 |  
 |  net_dormancy
 |      type: NetDormancy [Read-Only]
 |      Dormancy setting for actor to take itself off of the replication list without being destroyed on clients.
 |  
 |  net_priority
 |      type: float [Read-Write]
 |      Priority for this actor when checking for replication in a low bandwidth or saturated situation, higher priority means it is more likely to replicate
 |  
 |  net_update_frequency
 |      type: float [Read-Write]
 |      How often (per second) this actor will be considered for replication, used to determine NetUpdateTime
 |  
 |  net_use_owner_relevancy
 |      type: bool [Read-Write]
 |      If actor has valid Owner, call Owner's IsNetRelevantFor and GetNetPriority
 |  
 |  only_relevant_to_owner
 |      type: bool [Read-Only]
 |      If true, this actor is only relevant to its owner. If this flag is changed during play, all non-owner channels would need to be explicitly closed.
 |  
 |  pivot_offset
 |      type: Vector [Read-Only]
 |      Local space pivot offset for the actor
 |  
 |  replicates
 |      type: bool [Read-Only]
 |      If true, this actor will replicate to remote machines
 |      see: SetReplicates()
 |  
 |  root_component
 |      type: SceneComponent [Read-Only]
 |      Collision primitive that defines the transform (location, rotation, scale) of this Actor.
 |  
 |  spawn_collision_handling_method
 |      type: SpawnActorCollisionHandlingMethod [Read-Write]
 |      Controls how to handle spawning this actor in a situation where it's colliding with something else. "Default" means AlwaysSpawn here.
 |  
 |  sprite_scale
 |      type: float [Read-Write]
 |      The scale to apply to any billboard components in editor builds (happens in any WITH_EDITOR build, including non-cooked games).
 |  
 |  tags
 |      type: Array(Name) [Read-Write]
 |      Array of tags that can be used for grouping and categorizing.
 |  
 |  ----------------------------------------------------------------------
 |  Methods inherited from Object:
 |  
 |  execute_ubergraph(...)
 |      x.execute_ubergraph(entry_point) -- Executes some portion of the ubergraph.
 |      param: entry_point (int32) -- The entry point to start code execution at.
 |  
 |  ----------------------------------------------------------------------
 |  Methods inherited from _ObjectBase:
 |  
 |  __hash__(...)
 |      x.__hash__() <==> hash(x)
 |  
 |  __init__(...)
 |      x.__init__(...) initializes x; see help(type(x)) for signature
 |  
 |  __str__(...)
 |      x.__str__() <==> str(x)
 |  
 |  cast(...)
 |      X.cast(object) -> UObject -- cast the given object to this Unreal object type
 |  
 |  get_class(...)
 |      x.get_class() -> UClass -- get the Unreal class of this instance
 |  
 |  get_editor_property(...)
 |      x.get_editor_property(name) -> object -- get the value of any property visible to the editor
 |  
 |  get_fname(...)
 |      x.get_fname() -> FName -- get the name of this instance
 |  
 |  get_full_name(...)
 |      x.get_full_name() -> str -- get the full name (class name + full path) of this instance
 |  
 |  get_name(...)
 |      x.get_name() -> str -- get the name of this instance
 |  
 |  get_outer(...)
 |      x.get_outer() -> UObject -- get the outer object from this instance (if any)
 |  
 |  get_outermost(...)
 |      x.get_outermost() -> UPackage -- get the outermost object (the package) from this instance
 |  
 |  get_path_name(...)
 |      x.get_path_name() -> str -- get the path name of this instance
 |  
 |  get_typed_outer(...)
 |      x.get_typed_outer(type) -> type() -- get the first outer object of the given type from this instance (if any)
 |  
 |  get_world(...)
 |      x.get_world() -> UWorld -- get the world associated with this instance (if any)
 |  
 |  modify(...)
 |      x.modify(bool) -> bool -- inform that this instance is about to be modified (tracks changes for undo/redo if transactional)
 |  
 |  rename(...)
 |      x.rename(name=None, outer=None) -> bool -- rename this instance
 |  
 |  set_editor_property(...)
 |      x.set_editor_property(name, value) -- set the value of any property visible to the editor, ensuring that the pre/post change notifications are called
 |  
 |  static_class(...)
 |      X.static_class() -> UClass -- get the Unreal class of this type
"""

['activate_reverb_effect',
 'apply_damage',
 'apply_point_damage',
 'apply_radial_damage',
 'apply_radial_damage_with_falloff',
 'are_any_listeners_within_range',
 'are_subtitles_enabled',
 'begin_deferred_actor_spawn_from_class',
 'begin_spawning_actor_from_blueprint',
 'begin_spawning_actor_from_class',
 'blueprint_predict_projectile_path_advanced',
 'blueprint_predict_projectile_path_by_object_type',
 'blueprint_predict_projectile_path_by_trace_channel',
 'blueprint_suggest_projectile_velocity',
 'break_hit_result',
 'cancel_async_loading',
 'cast',
 'clear_sound_mix_class_override',
 'clear_sound_mix_modifiers',
 'create_player',
 'create_save_game_object',
 'create_save_game_object_from_blueprint',
 'create_sound2d',
 'deactivate_reverb_effect',
 'delete_game_in_slot',
 'deproject_screen_to_world',
 'does_save_game_exist',
 'enable_live_streaming',
 'execute_ubergraph',
 'find_collision_uv',
 'finish_spawning_actor',
 'flush_level_streaming',
 'get_accurate_real_time',
 'get_actor_array_average_location',
 'get_actor_array_bounds',
 'get_all_actors_of_class',
 'get_all_actors_with_interface',
 'get_all_actors_with_tag',
 'get_audio_time_seconds',
 'get_class',
 'get_current_level_name',
 'get_current_reverb_effect',
 'get_editor_property',
 'get_fname',
 'get_full_name',
 'get_game_instance',
 'get_game_mode',
 'get_game_state',
 'get_global_time_dilation',
 'get_int_option',
 'get_key_value',
 'get_name',
 'get_object_class',
 'get_outer',
 'get_outermost',
 'get_path_name',
 'get_platform_name',
 'get_player_camera_manager',
 'get_player_character',
 'get_player_controller',
 'get_player_controller_id',
 'get_player_pawn',
 'get_real_time_seconds',
 'get_streaming_level',
 'get_surface_type',
 'get_time_seconds',
 'get_typed_outer',
 'get_unpaused_time_seconds',
 'get_world',
 'get_world_delta_seconds',
 'get_world_origin_location',
 'grass_overlapping_sphere_count',
 'has_launch_option',
 'has_option',
 'is_game_paused',
 'load_game_from_slot',
 'load_stream_level',
 'make_hit_result',
 'modify',
 'open_level',
 'parse_option',
 'play_dialogue2d',
 'play_dialogue_at_location',
 'play_sound2d',
 'play_sound_at_location',
 'play_world_camera_shake',
 'pop_sound_mix_modifier',
 'project_world_to_screen',
 'push_sound_mix_modifier',
 'rebase_local_origin_onto_zero',
 'rebase_zero_origin_onto_local',
 'remove_player',
 'rename',
 'save_game_to_slot',
 'set_base_sound_mix',
 'set_editor_property',
 'set_game_paused',
 'set_global_listener_focus_parameters',
 'set_global_pitch_modulation',
 'set_global_time_dilation',
 'set_player_controller_id',
 'set_sound_mix_class_override',
 'set_subtitles_enabled',
 'set_world_origin_location',
 'spawn_decal_at_location',
 'spawn_decal_attached',
 'spawn_dialogue2d',
 'spawn_dialogue_at_location',
 'spawn_dialogue_attached',
 'spawn_emitter_at_location',
 'spawn_emitter_attached',
 'spawn_force_feedback_at_location',
 'spawn_force_feedback_attached',
 'spawn_object',
 'spawn_sound2d',
 'spawn_sound_at_location',
 'spawn_sound_attached',
 'static_class',
 'suggest_projectile_velocity_custom_arc',
 'unload_stream_level',
 '_post_init',
 '_wrapper_meta_data',
 'cache_ahead',
 'cache_behind',
 'cache_behind_game',
 'can_pause',
 'can_play_source',
 'can_play_url',
 'cast',
 'close',
 'execute_ubergraph',
 'get_audio_track_channels',
 'get_audio_track_sample_rate',
 'get_audio_track_type',
 'get_class',
 'get_desired_player_name',
 'get_duration',
 'get_editor_property',
 'get_fname',
 'get_full_name',
 'get_horizontal_field_of_view',
 'get_media_name',
 'get_name',
 'get_num_track_formats',
 'get_num_tracks',
 'get_outer',
 'get_outermost',
 'get_path_name',
 'get_player_name',
 'get_playlist',
 'get_playlist_index',
 'get_rate',
 'get_selected_track',
 'get_supported_rates',
 'get_time',
 'get_track_display_name',
 'get_track_format',
 'get_track_language',
 'get_typed_outer',
 'get_url',
 'get_vertical_field_of_view',
 'get_video_track_aspect_ratio',
 'get_video_track_dimensions',
 'get_video_track_frame_rate',
 'get_video_track_frame_rates',
 'get_video_track_type',
 'get_view_rotation',
 'get_world',
 'has_error',
 'is_buffering',
 'is_connecting',
 'is_looping',
 'is_paused',
 'is_playing',
 'is_preparing',
 'is_ready',
 'loop',
 'modify',
 'native_audio_out',
 'next',
 'open_file',
 'open_playlist',
 'open_playlist_index',
 'open_source',
 'open_url',
 'pause',
 'play',
 'play_on_open',
 'playlist',
 'playlist_index',
 'previous',
 'rename',
 'reopen',
 'rewind',
 'seek',
 'select_track',
 'set_desired_player_name',
 'set_editor_property',
 'set_looping',
 'set_rate',
 'set_track_format',
 'set_video_track_frame_rate',
 'set_view_field',
 'set_view_rotation',
 'shuffle',
 'static_class',
 'supports_rate',
 'supports_scrubbing',
 'supports_seeking',
 '__subclasshook__',
 '_post_init',
 '_wrapper_meta_data',
 'actor_has_tag',
 'add_actor_local_offset',
 'add_actor_local_rotation',
 'add_actor_local_transform',
 'add_actor_world_offset',
 'add_actor_world_rotation',
 'add_actor_world_transform',
 'add_component',
 'add_tick_prerequisite_actor',
 'add_tick_prerequisite_component',
 'always_relevant',
 'attach_to_actor',
 'attach_to_component',
 'auto_destroy_when_finished',
 'can_be_damaged',
 'cast',
 'custom_time_dilation',
 'destroy_actor',
 'destroy_component',
 'detach_from_actor',
 'disable_input',
 'enable_input',
 'execute_ubergraph',
 'find_camera_component_when_view_target',
 'flush_net_dormancy',
 'force_net_update',
 'generate_overlap_events_during_level_streaming',
 'get_actor_bounds',
 'get_actor_enable_collision',
 'get_actor_eyes_view_point',
 'get_actor_forward_vector',
 'get_actor_label',
 'get_actor_location',
 'get_actor_relative_scale3d',
 'get_actor_right_vector',
 'get_actor_rotation',
 'get_actor_scale3d',
 'get_actor_tick_interval',
 'get_actor_time_dilation',
 'get_actor_transform',
 'get_actor_up_vector',
 'get_all_child_actors',
 'get_attach_parent_actor',
 'get_attach_parent_socket_name',
 'get_attached_actors',
 'get_class',
 'get_component_by_class',
 'get_components_by_class',
 'get_components_by_tag',
 'get_distance_to',
 'get_dot_product_to',
 'get_editor_property',
 'get_fname',
 'get_folder_path',
 'get_full_name',
 'get_game_time_since_creation',
 'get_horizontal_distance_to',
 'get_horizontal_dot_product_to',
 'get_input_axis_key_value',
 'get_input_axis_value',
 'get_input_vector_axis_value',
 'get_instigator',
 'get_instigator_controller',
 'get_life_span',
 'get_name',
 'get_outer',
 'get_outermost',
 'get_overlapping_actors',
 'get_overlapping_components',
 'get_owner',
 'get_parent_actor',
 'get_parent_component',
 'get_path_name',
 'get_remote_role',
 'get_squared_distance_to',
 'get_tickable_when_paused',
 'get_typed_outer',
 'get_velocity',
 'get_vertical_distance_to',
 'get_world',
 'has_authority',
 'hidden',
 'initial_life_span',
 'instigator',
 'is_actor_being_destroyed',
 'is_actor_tick_enabled',
 'is_child_actor',
 'is_editable',
 'is_hidden_ed',
 'is_hidden_ed_at_startup',
 'is_overlapping_actor',
 'is_selectable',
 'is_temporarily_hidden_in_editor',
 'make_mid_for_material',
 'make_noise',
 'min_net_update_frequency',
 'modify',
 'net_cull_distance_squared',
 'net_dormancy',
 'net_priority',
 'net_update_frequency',
 'net_use_owner_relevancy',
 'on_become_view_target',
 'on_end_view_target',
 'on_reset',
 'only_relevant_to_owner',
 'pivot_offset',
 'prestream_textures',
 'receive_actor_begin_cursor_over',
 'receive_actor_begin_overlap',
 'receive_actor_end_cursor_over',
 'receive_actor_end_overlap',
 'receive_actor_on_clicked',
 'receive_actor_on_input_touch_begin',
 'receive_actor_on_input_touch_end',
 'receive_actor_on_input_touch_enter',
 'receive_actor_on_input_touch_leave',
 'receive_actor_on_released',
 'receive_any_damage',
 'receive_begin_play',
 'receive_destroyed',
 'receive_end_play',
 'receive_hit',
 'receive_point_damage',
 'receive_radial_damage',
 'receive_tick',
 'remove_tick_prerequisite_actor',
 'remove_tick_prerequisite_component',
 'rename',
 'replicates',
 'root_component',
 'set_actor_enable_collision',
 'set_actor_hidden_in_game',
 'set_actor_label',
 'set_actor_location',
 'set_actor_location_and_rotation',
 'set_actor_relative_location',
 'set_actor_relative_rotation',
 'set_actor_relative_scale3d',
 'set_actor_relative_transform',
 'set_actor_rotation',
 'set_actor_scale3d',
 'set_actor_tick_enabled',
 'set_actor_tick_interval',
 'set_actor_transform',
 'set_editor_property',
 'set_folder_path',
 'set_is_temporarily_hidden_in_editor',
 'set_life_span',
 'set_net_dormancy',
 'set_owner',
 'set_replicate_movement',
 'set_replicates',
 'set_tick_group',
 'set_tickable_when_paused',
 'spawn_collision_handling_method',
 'sprite_scale',
 'static_class',
 'tags',
 'tear_off',
 'teleport',
 'user_construction_script',
 'was_recently_rendered'
 ]

import sys; sys.path.append("/Users/shosumioka/Documents/Yurlungur"); import yurlungur as yr;

yr.log("aaa")

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


# command
# class PyHelloWorldCmd(om.MPxCommand):
#     kPluginCmdName = "pyHelloWorld"
#
#     def __init__(self):
#         om.MPxCommand.__init__(self)
#
#     @staticmethod
#     def cmdCreator():
#         return PyHelloWorldCmd()
#
#     def doIt(self, args):
#         print ("Hello World!")


# Initialize the plug-in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            PyHelloWorldCmd.kPluginCmdName, PyHelloWorldCmd.cmdCreator
        )
    except:
        sys.stderr.write(
            "Failed to register command: %s\n" % PyHelloWorldCmd.kPluginCmdName
        )
        raise


# Uninitialize the plug-in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(PyHelloWorldCmd.kPluginCmdName)
    except:
        sys.stderr.write(
            "Failed to unregister command: %s\n" % PyHelloWorldCmd.kPluginCmdName
        )
        raise


# import maya.cmds as cmds
#
# cmds.loadPlugin("C:/Users/sumiosho/Desktop/tools/test.py")
# cmds.pyHelloWorld()

# blender

plugin_info = {
    "name": "sample: add-onTest",
    "author": "ssss",
    "version": (2, 0),
    "blender": (2, 79, 0),
    "location": "",
    "description": "sample",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


def register():
    print("sample: add-onTest ON")


def unregister():
    print("sample: add-onTest OFF")


if __name__ == "__main__":
    register()


EGG_FILENAME = "/Users/shosumioka/Library/Application Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/181.5087.37/PyCharm.app/Contents/debug-eggs/pycharm-debug.egg"
PYD = "/Users/shosumioka/Library/Application/ Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/181.5087.37/PyCharm.app/Contents/helpers/pydev"
HOST = 'localhost'
PORT = 9999

# PyCharm付属のeggファイルにパスを通す
import sys
if EGG_FILENAME not in sys.path:
    sys.path.append(EGG_FILENAME)
    sys.path.append(PYD)

# 起動
import pydevd
pydevd.settrace(HOST, port=PORT, stdoutToServer=True, stderrToServer=True)