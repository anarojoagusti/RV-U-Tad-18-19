#define STB_IMAGE_IMPLEMENTATION

#include "../lib/glew/glew.h"
#include "../lib/glfw3/glfw3.h"
#include "Buffer.h"
#include "Shader.h"
#include "Vertex.h"
#include "State.h"
#include "World.h"
#include "Mesh.h"
#include "Model.h"
#include "Camera.h"
#include "Material.h"
#include "Entity.h"
#include "Light.h"
#include <memory>
#include "../lib/glm/glm.hpp"
#include "../lib/glm/gtc/matrix_transform.hpp"
#include "../lib/glm/gtc/random.hpp"
#include "../lib/glm/gtc/type_ptr.hpp"
#include "../lib/glm/gtx/string_cast.hpp"
#include <array>
#include <fstream>
#include <iostream>
#include <sstream>

//Lectura de archivos
std::string readString(const char *filename) {
    std::ifstream f(filename, std::ios_base::binary);
    std::stringstream ss;
    ss << f.rdbuf();
    return ss.str();
}
#define FULLSCREEN false

//Inicializacion del motor
bool init() {
    // Init GLEW
    if (glewInit() != 0) {
        std::cout << "could not initialize glew" << std::endl;
        return false;
    }

    //Habilito OpenGL States
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_SCISSOR_TEST);
	glEnable(GL_BLEND);
	glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS);

	//Generación del shader por defecto 
	std::string vertexShader = readString("../data/vertex.shd");
	std::string fragmentShader = readString("../data/fragment.shd");
	Shader shader(vertexShader, fragmentShader);
    shader.use();

	State::defaultShader = std::make_shared<Shader>(shader);

	return true;
}

int main() {

	// Init GLFW para generar la ventana
	if (glfwInit() != GLFW_TRUE) {
		std::cout << "could not initalize glfw" << std::endl;
		return false;
	}

	// Creo la ventana
    GLFWwindow *window = glfwCreateWindow(800, 600, "Ana Rojo Window", FULLSCREEN ? glfwGetPrimaryMonitor() : nullptr, nullptr);
    if (window == nullptr) {
        std::cout << "could not create glfw window" << std::endl;
        return -15;
    }
    glfwMakeContextCurrent(window);

	//Compruebo que el motor ha sido inicializado
	if (!init()) {
		return -10;
	}

    atexit(glfwTerminate);

	// Creo el mundo
	std::shared_ptr<World> world = std::make_shared<World>();

	// Creo la cámara
	std::shared_ptr<Camera> mainCamera = std::make_shared<Camera>();
	mainCamera->setClearColor(glm::vec3(0.0f, 0.0f, 0.0f));
	mainCamera->setPosition(glm::vec3(0.0f, 0.0f, 0.0f));
	glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
 
	mainCamera->setUpdate([mainCamera, window](float dt) {
        if (glfwGetKey(window, GLFW_KEY_W)) {
            mainCamera->move(glm::vec3(0.0f, 0.0f, -1.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_A)) {
            mainCamera->move(glm::vec3(-1.0f, 0.0f, 0.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_S)) {
            mainCamera->move(glm::vec3(0.0f, 0.0f, 1.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_D)) {
            mainCamera->move(glm::vec3(1.0f, 0.0f, 0.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_SPACE)) {
            mainCamera->move(glm::vec3(0.0f, 1.0f, 0.0f)*dt);
        }
        if (glfwGetKey(window, GLFW_KEY_LEFT_CONTROL) || glfwGetKey(window, GLFW_KEY_RIGHT_CONTROL)) {
            mainCamera->move(glm::vec3(0.0f, -1.0f, 0.0f)*dt);
        }

        glm::ivec4 halfVP = mainCamera->getViewport()/2;
        glm::vec2 viewportCenter = { halfVP.z, halfVP.w };


        double xpos = 0, ypos = 0;
        glfwGetCursorPos(window, &xpos, &ypos);
        glm::vec2 currMousePos(xpos, ypos);
        currMousePos = (viewportCenter - currMousePos) / viewportCenter;
        
        glm::quat xQuad = glm::rotate(glm::quat(), currMousePos.x, glm::vec3(0.0f, 1.0f, 0.0f));
        glm::quat yQuad = glm::rotate(glm::quat(), currMousePos.y, glm::vec3(1.0f, 0.0f, 0.0f));
        mainCamera->setRotation(xQuad * yQuad);
	});
	world->addEntity(mainCamera);

	//// Cargo la malla Bunny
	std::shared_ptr<Mesh> meshBunny = Mesh::load("../data/bunny.msh.xml");
	std::shared_ptr<Model> modelBunny = std::make_shared<Model>(meshBunny);
	modelBunny->setScale(glm::vec3(5.0f, 5.0f, 5.0f));
	modelBunny->setPosition(glm::vec3(0.0f, 0.0f, 0.0f));
	modelBunny->setRotation(glm::vec3(90.0f, 0.0f, 0.0f));
	world->addEntity(modelBunny);

	//// Luz ambiente
	world->setAmbient(glm::vec3(0.2f, 0.2f, 0.2f));
	//Luz puntual
	std::shared_ptr<Light> pLight = std::make_shared<Light>(Light::Type::POINT, glm::vec3(1, 1, 1));
	pLight->setColor(glm::vec3(1.0, 0.0, 0.0)); //rojo
	pLight->setLinearAttenuation(0.2);
	world->addEntity(pLight);
	//Luz direccional
	std::shared_ptr<Light> dLight = std::make_shared<Light>(Light::Type::DIRECTIONAL, glm::vec3(1, 1, 1));
	dLight->setColor(glm::vec3(1.0, 1.0, 1.0));
	world->addEntity(dLight);

	glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
	double lastMX, lastMY;
	glfwGetCursorPos(window, &lastMX, &lastMY);

	auto lastTime = static_cast<float>(glfwGetTime());
	float accumulatedTime = 0.0f;
	while (glfwWindowShouldClose(window) == 0 && glfwGetKey(window, GLFW_KEY_ESCAPE) == 0) {
		// Update delta time
		auto newTime = static_cast<float>(glfwGetTime());
		float deltaTime = newTime - lastTime;
		lastTime = newTime;
		accumulatedTime += deltaTime;

		// Get updated screen size
		int screenWidth, screenHeight;
		glfwGetWindowSize(window, &screenWidth, &screenHeight);

		int frameBufferWidth, frameBufferHeight;
		glfwGetFramebufferSize(window, &frameBufferWidth, &frameBufferHeight);

		double mouseX, mouseY;
		glfwGetCursorPos(window, &mouseX, &mouseY);
		float speedMX = static_cast<int>(mouseX - lastMX);
		float speedMY = static_cast<int>(mouseY - lastMY);
		lastMX = mouseX;
		lastMY = mouseY;

		glm::vec3 pos = pLight->getPosition();
		for (int i = 0; i < world->getNumEntities(); ++i) {
			std::shared_ptr<Light> isLight = std::dynamic_pointer_cast<Light>(world->getEntity(i));

			if (!isLight) {}
			else {

				pLight->setRotation(glm::vec3(pLight->getRotation().x - speedMY, pLight->getRotation().y - speedMX, 0));

				if (glfwGetKey(window, GLFW_KEY_W)) {
					pLight->move(glm::vec3(0, 0, -deltaTime * 2));
				}
				if (glfwGetKey(window, GLFW_KEY_S)) {
					pLight->move(glm::vec3(0, 0, deltaTime * 2));
				}
				if (glfwGetKey(window, GLFW_KEY_A)) {
					pLight->move(glm::vec3(-deltaTime * 2, 0, 0));
				}
				if (glfwGetKey(window, GLFW_KEY_D)) {
					pLight->move(glm::vec3(deltaTime * 2, 0, 0));
				}
			}
		}

		pLight->setPosition(glm::vec3(0.0f, 0.5f, -0.5f));
		pLight->setRotation(glm::vec3(0, accumulatedTime * 10, 10));
		pLight->move(glm::vec3(0.0f, 0.0f, 5.0f));

		mainCamera->setPosition(glm::vec3(0.0f, 0.3f, 1.0f));
		mainCamera->setProjection(glm::perspective(glm::radians(90.0f), static_cast<float>(screenWidth) / static_cast<float>(screenHeight), 0.1f, 100.0f));
		mainCamera->setViewport(glm::ivec4(0, 0, screenWidth, screenHeight));
		//Preparo segun la posicion de la cámara, actualizo los valores State
		mainCamera->prepare();
		//Pinto en la ventana
		world->update(deltaTime);
		world->draw();

        // Swapeo buffers y actualizo eventos
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    return 0;
}
