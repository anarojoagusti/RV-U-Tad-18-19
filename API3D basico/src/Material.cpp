#include "Material.h"
#include "State.h"

Material::Material(const std::shared_ptr<Texture>& tex, const std::shared_ptr<Shader>& shader) : shader(shader), texture(tex) {}

const std::shared_ptr<Shader>& Material::getShader() const {
	if (Material::shader == nullptr) {
		return State::defaultShader;
	}

	return Material::shader;
}

std::shared_ptr<Shader>& Material::getShader() {
	return Material::shader == nullptr ? State::defaultShader : Material::shader;
}

void Material::setShader(const std::shared_ptr<Shader>& shader) {
	Material::shader = shader;
}

const std::shared_ptr<Texture>& Material::getTexture() const {
	return Material::texture;
}

void Material::setTexture(const std::shared_ptr<Texture>& tex) {
	Material::texture = tex;
}

void Material::prepare() {
	auto shader = getShader();
	shader->use();

	glm::mat4 model = State::modelMatrix;
	glm::mat4 view = State::viewMatrix;
	glm::mat4 projection = State::projectionMatrix;

	glm::mat4 MVP = projection * view * model;
	glm::mat4 MV = view * model;
	glm::mat4 normalMat = glm::transpose(glm::inverse(MV));

	// Matrix Modelo Vista Proyeccion MVP
	int locMVP = shader->getLocation("MVP");
	shader->setMatrix(locMVP, MVP);

	//Matriz MV - Transformacion de las coordenas al espacio del observador (camara) para el calculo de luces
	int locMV = shader->getLocation("MV");
	shader->setMatrix(locMV, MV);

	int locNormalMat = shader->getLocation("normalMat");
	shader->setMatrix(locNormalMat, normalMat);

	// Matriz Modelo
	int locM = shader->getLocation("M");
	shader->setMatrix(locM, model);

	// Vector3 posicion del observador
	int locEyePos = shader->getLocation("eyePos");
	shader->setVec3(locEyePos, State::eyePos);

	int locNumLights = shader->getLocation("numLights");
	shader->setInt(locNumLights, State::lights.size());

	// Color difuso de material activo
	int locMatColor = shader->getLocation("matColor");
	shader->setVec4(locMatColor, Material::color);

	// Color especular de un material activo
	int locMatShine = shader->getLocation("matShine");
	shader->setInt(locMatShine, Material::shininess);

	// Luz ambiente
	int locAmbientLight = shader->getLocation("ambientLight");
	shader->setVec3(locAmbientLight, State::ambient);

	// Textura
	int locTS = shader->getLocation("texSampler");
	shader->setInt(locTS, 0);
	int locCTS = shader->getLocation("cubeTexSampler");
	shader->setInt(locCTS, 1);

	int isTexture = shader->getLocation("isTexturized");
	auto texture = getTexture();
	if (texture != nullptr) {
		int locIsCube = shader->getLocation("isCube");
		shader->setInt(locIsCube, texture->isCube());

		shader->setInt(isTexture, true);
		if (!texture->isCube()) {
			texture->bind(0);
		} else { //Cube
			texture->bind(1);
		}
	} else {
		shader->setInt(isTexture, false);
	}

	//Material Mode
	if (materialMode == MaterialMode::ALPHA) glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	else if (materialMode == MaterialMode::ADD) glBlendFunc(GL_SRC_ALPHA, GL_ONE);
	else if (materialMode == MaterialMode::MUL) glBlendFunc(GL_ZERO, GL_SRC_COLOR);

	// Cubemaps
	// Reflection
	auto reflectionTexture = getReflectionTexture();
	int locReflection = shader->getLocation("reflectionTex");
	shader->setInt(locReflection, 2);
	int locHasReflectionTex = shader->getLocation("hasReflectionTex");
	shader->setInt(locHasReflectionTex, reflectionTexture ? true : false);
	if (reflectionTexture != nullptr) {
		reflectionTexture->bind(2);
	}

	// Refraction
	auto refractionTexture = getRefractionTexture();
	int locRefraction = shader->getLocation("refractionTex");
	shader->setInt(locRefraction, 3);
	int locHasRefractionTex = shader->getLocation("hasRefractionTex");
	shader->setInt(locHasRefractionTex, refractionTexture ? true : false);
	if (refractionTexture != nullptr) {
		refractionTexture->bind(3);

		// Refraction coefficient
		int locRefractionCoef = shader->getLocation("refractionCoef");
		shader->setFloat(locRefractionCoef, refractionCoef);
	}


	// Normal
	auto normalTexture = getNormalTexture();
	int locNormalTex = shader->getLocation("normalTex");
	shader->setInt(locNormalTex, 4);
	int locHasNormalTex = shader->getLocation("hasNormalTex");
	shader->setInt(locHasNormalTex, normalTexture ? true : false);
	if (normalTexture != nullptr) {
			normalTexture->bind(4);
	}

}

const glm::vec4& Material::getColor() const {
	return Material::color;
}

void Material::setColor(const glm::vec4& color) {
	Material::color = color;
}

uint8_t Material::getShininess() const {
	return Material::shininess;
}

void Material::setShininess(uint8_t shininess) {
	Material::shininess = shininess;
}

MaterialMode Material::getMode() const
{
	return MaterialMode();
}

void Material::setMode(MaterialMode materialMode) {
	Material::materialMode = materialMode;
}

const std::shared_ptr<Texture>& Material::getReflectionTexture() const {
	return Material::reflectionTexture;
}

void Material::setReflectionTexture(const std::shared_ptr<Texture>& tex) {
	reflectionTexture = tex;
}

const std::shared_ptr<Texture>& Material::getRefractionTexture() const {
	return refractionTexture;
}

void Material::setRefractionTexture(const std::shared_ptr<Texture>& tex) {
	refractionTexture = tex;
}

const std::shared_ptr<Texture>& Material::getNormalTexture() const {
	return normalTexture;
}

void Material::setNormalTexture(const std::shared_ptr<Texture>& tex) {
	normalTexture = tex;
}

float Material::getRefractionCoef() const {
	return refractionCoef;
}

void Material::setRefractionCoef(float coef) {
	refractionCoef = coef;
}
