# Field explanation

### `package`
Represents the file itself.

```yaml
package:
  id: bubbletea
  name: Bubble Tea
  language: go
  type: framework
```

### `type`
Allowed values:
- framework
- library
- package
- sdk
- runtime
- tool

This doesn't describe repositories. It describes what the package is.

### `metadata`
```yaml
metadata:
  aliases:
    - bubble-tea
  tags:
    - tui
    - terminal
    - cli
```
Used for searching.

### `repositories`
This is the important part.

```yaml
repositories:
  - owner: charmbracelet
    repo: bubbletea-app-template
```

### `kind`
What the repository actually is.

Allowed values:
- template
- starter
- boilerplate
- example
- reference
- showcase
- component

Notice: No framework, library, or package because those belong to the package, not the repository.

### `stack`
The stack inside the repository.

```yaml
stack:
  - bubbletea
  - bubbles
  - cobra
  - viper
```
This is how future searching works.

### `tags`
Repository-level tags.

Example:
```yaml
tags:
  - auth
  - postgres
  - docker
  - websocket
```

### `official`
```yaml
official: true
```
Maintained by the package creators.

### `verified`
Your project has reviewed it.

### `priority`
Manual ranking.
- 100 Official
- 90  Highly recommended
- 70  Popular
- 50  Default
- 30  Experimental

This helps search quality.

### `notes`
Optional.

```yaml
notes: Production ready.
```
or
```yaml
notes: Archived but still useful.
```

# Complete example
```yaml
version: 1

package:
  id: bubbletea
  name: Bubble Tea
  language: go
  type: framework

metadata:
  aliases:
    - bubble-tea
  tags:
    - tui
    - terminal
    - cli

repositories:
  - owner: charmbracelet
    repo: bubbletea-app-template
    kind: template
    stack:
      - bubbletea
      - bubbles
      - lipgloss
    tags:
      - production
      - starter
    official: true
    verified: true
    priority: 100

  - owner: charmbracelet
    repo: wishlist
    kind: example
    stack:
      - bubbletea
    tags:
      - demo
    official: true
    verified: true
    priority: 90
```
