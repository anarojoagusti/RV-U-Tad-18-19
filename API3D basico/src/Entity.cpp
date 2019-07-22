#include "Entity.h"

Entity::Entity() {}

const glm::vec3 & Entity::getPosition() const
{
	return Entity::position;
}

void Entity::setPosition(const glm::vec3 & pos)
{
	Entity::position = pos;
}

const glm::vec3 & Entity::getScale() const
{
	return Entity::scale;
}

const void Entity::setRotation(const glm::quat& rot) {
	 rotation = rot;
}

void Entity::setScale(const glm::vec3 & scale)
{
	Entity::scale = scale;
}

void Entity::move(const glm::vec3 & vec)
{
	position += rotation * vec;
}

void Entity::setUpdate(std::function<void(float)> updateFunction) {
	updateEntity = updateFunction;
}

