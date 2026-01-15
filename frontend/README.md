# Chatbot Platform - React Frontend

A modern React frontend for ChatBot Platform.

## Quick Start

### Installation

```bash
cd frontend
npm install
```

### Start Development Server

```bash
npm start
```

Opens at `http://localhost:3000`

## Clean Installation

If you had the old version installed:

```bash
# Remove old dependencies
rm -rf node_modules package-lock.json

# Fresh install
npm install

# Verify no critical vulnerabilities
npm audit
```

## Verification

After installation, you should see:

```bash
npm audit
# found 0 vulnerabilities (or only low-severity)
```

## ESLint Warnings Fixed

✅ **Fixed:** React Hook `useEffect` dependency warnings by using `useCallback`
✅ **No more warnings** during compilation

## Development

All features from the original version:

- ✅ Authentication (login/register)
- ✅ Project management
- ✅ System prompts
- ✅ Chat interface with **proper isolation per project**
- ✅ Clean, modern UI

## Project Structure

```sh
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── AuthPage.js
│   │   ├── Sidebar.js
│   │   ├── ChatInterface.js
│   │   ├── PromptsManager.js         # Fixed hooks
│   │   └── CreateProjectModal.js
│   ├── services/
│   │   └── api.js
│   ├── App.js                         # Fixed hooks
│   ├── App.css
│   └── index.js
├── package.json                       # Updated dependencies
├── .env.example
└── .gitignore
```

## Environment Configuration

Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Production Build

```bash
npm run build
```

Creates optimized build in `build/` folder.

## Troubleshooting


1. Delete `node_modules` and `package-lock.json`:
   ```bash
   rm -rf node_modules package-lock.json
   ```

2. Clear npm cache:
   ```bash
   npm cache clean --force
   ```

3. Reinstall:
   ```bash
   npm install
   ```

### Audit shows warnings but not errors?

The package.json includes `overrides` to force secure versions of transitive dependencies. Some warnings may still appear for dev dependencies that don't affect production.

## Scripts

- `npm start` - Start development server
- `npm build` - Create production build  
- `npm test` - Run tests
- `npm run eject` - Eject from CRA (not recommended)


## License

MIT
