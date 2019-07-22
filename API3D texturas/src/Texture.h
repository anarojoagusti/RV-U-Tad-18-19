#pragma once

#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <memory>
#include "stb_image.h"
#include "../lib/glew/glew.h"
#include "../lib/glfw3/glfw3.h"
#include <iostream>

class Texture  {
private:
	uint32_t id;
	uint32_t width;
	uint32_t height;
	std::shared_ptr<void*> img;
	bool cube;

public:
	Texture(uint32_t id, uint32_t width, uint32_t height, bool isCube);
    ~Texture();
	//Carga de texturas 2D
	static std::shared_ptr<Texture>	load(const char* filename);

	uint32_t getId() const;
	const glm::ivec2& getSize() const;

	//Carga de texturas cubeMapping
	static std::shared_ptr<Texture> load(const char* left, const char* right, const char* front, const char* back, const char* top, const char* bottom);

	//Bindear aristas del cubo
	void bind(int layer = 0) const;
	bool isCube() const;

};
