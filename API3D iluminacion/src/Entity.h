#pragma once

#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <memory>
#include <functional>
#include <sstream>
#include <fstream>

class Entity {
protected:
	glm::vec3 position;
	glm::vec3 scale;
	glm::quat rotation;

	std::function<void(float)> updateEntity;

public:
	Entity();
	virtual ~Entity() {}

	const glm::vec3& getPosition() const;
	void setPosition(const glm::vec3& pos);
	const glm::vec3& getScale() const;
	void setScale(const glm::vec3& scale);
	const glm::quat& getRotation() const;
	const void setRotation(const glm::quat& rot);
	void setUpdate(const std::function<void(float)> updateFunc);
	void move(const glm::vec3& vec);	
	virtual void update(float deltaTime) { if (updateEntity) updateEntity(deltaTime); }
	virtual void draw() {}
};
