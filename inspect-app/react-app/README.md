# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.
## Teleprompt

### Purpose and Philosophy

Teleprompt is designed to facilitate human-computer interaction through natural language by providing a framework for prompting language models in a more structured and deliberate fashion. Its philosophical basis lies in the recognition that human language is a critical tool for directing AI behavior. By systematically crafting prompts, teleprompt aims to leverage the underlying capabilities of powerful language models to generate text that is more aligned with the user's intent and context.

### How It Achieves Its Purpose

Teleprompt achieves its purpose through a range of features designed to fine-tune the way prompts are presented to language models. For instance, it includes mechanisms for setting the tone, style, and formality of the prompt, adjusting ambiguity levels, and embedding contextual cues. This meticulous control allows for more predictable and useful outputs from the language model.

### Examples

To use teleprompt, you first create a prompt configuration, which determines the characteristics of the generated text. Then, invoke the language model with the prompt to receive the output. Here's a pseudocode example:

```javascript
// Initialize the teleprompt configuration
let promptConfig = new dspy.TelepromptConfig({
    tone: 'informative',
    style: 'professional',
    formality: true,
    ambiguity: 'low'
});

// Create the prompt using teleprompt
let prompt = dspy.createTeleprompt({
    inputText: "Explain the concept of gravitational waves.",
    config: promptConfig
});

// Invoke the language model
let output = lm(prompt);
console.log(output);
```

Note: Actual code will vary based on the language model and teleprompt API specifics.

Please refer to the accompanying Jupyter notebooks for real-case scenarios and detailed examples.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
