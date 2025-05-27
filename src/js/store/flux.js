const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			personas: ["Pedro","Maria"]
		},
		actions: {

			exampleFunction: () => {
                    console.log("hola")
                    return
			},
		}
	};
};

export default getState;