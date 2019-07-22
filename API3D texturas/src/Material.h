#pragma once

#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <memory>
#include "Texture.h"
#include "Shader.h"

enum MaterialMode {
	ALPHA,
	ADD,
	MUL
};

class Material  {
private:

	std::shared_ptr<Shader> shader;
	std::shared_ptr<Texture> texture;

	glm::vec4 color = glm::vec4(1.0f, 1.0f, 1.0f, 1.0f);
	int shininess;

	MaterialMode materialMode = ALPHA;
	bool lighting = true;

	std::shared_ptr<Texture> reflectionTexture;
	std::shared_ptr<Texture> refractionTexture;
	std::shared_ptr<Texture> normalTexture;
	float refractionCoef;

public:
	Material(const std::shared_ptr<Texture>& tex = nullptr,
		const std::shared_ptr<Shader>& shader = nullptr);
	const std::shared_ptr<Shader>& getShader() const;
	std::shared_ptr<Shader>& getShader();
	void setShader(const std::shared_ptr<Shader>& shader);
	const std::shared_ptr<Texture>& getTexture() const;
	void setTexture(const std::shared_ptr<Texture>& tex);
	void prepare();

	const glm::vec4& getColor() const;
	void setColor(const glm::vec4& color);
	uint8_t getShininess() const;
	void setShininess(uint8_t shininess);

	MaterialMode getMode() const;
	void setMode(MaterialMode materialMode);

	bool getLighting() const;
	void setLighting(bool enable);

	const std::shared_ptr<Texture>& getReflectionTexture() const;
	void setReflectionTexture(const std::shared_ptr<Texture>& tex);

	const std::shared_ptr<Texture>& getRefractionTexture() const;
	void setRefractionTexture(const std::shared_ptr<Texture>& tex);

	const std::shared_ptr<Texture>& getNormalTexture() const;
	void setNormalTexture(const std::shared_ptr<Texture>& tex);

	float getRefractionCoef() const;
	void setRefractionCoef(float coef);
};

