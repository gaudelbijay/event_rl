
#include <gazebo/gazebo.hh>
#include <ignition/math.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <stdio.h>

namespace gazebo
{
  class DynamicMale : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      this->model = _parent;

      gazebo::common::PoseAnimationPtr anim(
          new gazebo::common::PoseAnimation("DynamicMale", 10.0, true));

      gazebo::common::PoseKeyFrame *key;

      key = anim->CreateKeyFrame(0.0);
      key->Translation(ignition::math::Vector3d(0, 0, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      key = anim->CreateKeyFrame(5.0);
      key->Translation(ignition::math::Vector3d(3, 3, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 1.57));

      key = anim->CreateKeyFrame(10.0);
      key->Translation(ignition::math::Vector3d(0, 0, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 3.14));

      this->model->SetAnimation(anim);
    }

    private: physics::ModelPtr model;
  };

  GZ_REGISTER_MODEL_PLUGIN(DynamicMale)
}
