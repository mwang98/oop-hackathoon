# Medicare Provider Finder Frontend

This is a React.js frontend for the Medicare Provider Finder application. It allows users to search for healthcare providers based on their zip code, Medicare number, symptoms, and availability.

## Features

- Search for providers by zip code
- Enter Medicare number for insurance coverage
- Describe symptoms to find appropriate specialists
- Specify availability for appointments
- View provider cards with available time slots
- In-network filtering

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend server running (FastAPI)

### Installation

1. Clone the repository (if not already done)
2. Install dependencies:

```bash
cd client
npm install
```

### Running the Application

1. Make sure the backend server is running first (typically on port 8000)
2. Start the React development server:

```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

### Building for Production

To create a production build:

```bash
npm run build
```

## Project Structure

- `src/components/` - React components
  - `ProviderSearch.js` - Search form component
  - `ProviderResults.js` - Results display component
- `src/services/` - API services
  - `providerService.js` - API calls to the backend

## API Integration

The frontend communicates with the FastAPI backend using the following endpoint:

- `POST /providers/recommend` - Get provider recommendations based on search criteria

## Technologies Used

- React.js
- React Router
- React Bootstrap
- Axios for API calls

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

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
