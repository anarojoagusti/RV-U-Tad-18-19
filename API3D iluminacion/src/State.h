#pragma once
#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <memory>
#include "../lib/glew/glew.h"
#include "../lib/glfw3/glfw3.h"
#include "Shader.h"
#include "Light.h"
#include <vector>

class State {
public:
	static std::shared_ptr<Shader> defaultShader;
	static glm::mat4 projectionMatrix;
	static glm::mat4 viewMatrix;
	static glm::mat4 modelMatrix;
	static std::vector<std::shared_ptr<Light>> lights;
	static glm::vec3 ambient;
	static glm::vec3 eyePos;
};
