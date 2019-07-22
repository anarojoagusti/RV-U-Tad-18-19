#pragma once 

#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <memory>
#include "Mesh.h"
#include "Entity.h"


class Model : public Entity {
private:
	std::shared_ptr<Mesh> mesh;

  public:
	  Model(const std::shared_ptr<Mesh>& mesh);
	  virtual void draw() override;
};
