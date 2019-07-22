#pragma once
#include "../lib/glew/glew.h"
#include "../lib/glfw3/glfw3.h"
#include "Shader.h"
#include "Vertex.h"
#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <memory>
#include <array>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

class Buffer {
  private:
    uint32_t buffers[2];
    std::vector<Vertex> vertices;
    std::vector<int> indices;

  public:
    Buffer(std::vector<Vertex> vertices, std::vector<int> indices);
    ~Buffer();
    void draw(const Shader &shader) const;
};
