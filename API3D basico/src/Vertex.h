#pragma once 

#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <memory>

class Vertex {
  public:
	Vertex();
	Vertex(const glm::vec3 position, const glm::vec2 coords, const glm::vec3 normal);
	Vertex(const glm::vec3 position, const glm::vec2 coords, const glm::vec3 normal, const glm::vec3 tan);
    glm::vec3 position;
	glm::vec2 text_coord;
	glm::vec3 normal;
	glm::vec3 tangent;
};
