#pragma once 
#include "../lib/glew/glew.h"
#include "../lib/glfw3/glfw3.h"

#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <memory>
#include "Vertex.h"
#include "string"
#include <array>
#include <fstream>
#include <iostream>
#include <sstream>

class Shader {
  private:

    uint32_t program;
    int vposLoc;
    int vtexLoc;
    int vnormalLoc;
    int vtangentLoc;
    uint32_t vs;
    uint32_t fs;

	char errorLog[1024];

  public:
    Shader(std::string const &vertexShader, std::string const &fragmentShader);
    ~Shader();

	uint32_t getId() const;
	const char *getError() const;
    void use() const;
    void setupAttribs() const;
	GLint getLocation(const char *name) const;

    void setInt(int loc, int val);
    void setFloat(int loc, float val);
    void setVec3(int loc, const glm::vec3 &vec);
    void setVec4(int loc, const glm::vec4 &vec);
    void setMatrix(int loc, const glm::mat4 &matrix);
};
