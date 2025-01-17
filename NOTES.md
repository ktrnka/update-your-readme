# Github Models

Dealbreaker:
Currently, the GITHUB_TOKEN associated with the action run doesn't have permissions to Github Models and there's no way to add those permissions. You can use a personal access token but to do so, you need the user to create one and add it to their secrets.

- To use structured output, you need to override the API version
- To use o1, you need to override it to a newer one
- gpt4o and gpt4o-mini work with structured output. No other models work with it that I've tried. They give back different errors
- The o1 family doesn't support the `system` message so the input needs to be prepared differently for the o1 family
- There's a helpful field showing whether the generation hit the length limit
- The schema has some weird issues

## TODO

- Code that inspects a repo and builds an evaluation set from the repo by seeing which auto-PRs were accepted or rejected
- More-flexible wrapper so that we can try out the o1 family


# Old
```suggestion
langchain = "*"
```

Note: The diffing for suggestion format doesn't work right

The GH Actions helps:
https://github.com/marketplace/actions/create-pull-request

# Repos tested

- This repo: Great results so far!
- Locust: It mostly fails with a Pydantic ValidationError, which is hiding some deeper problem
- DVC: This is RST not MD so the code fails to find it in the first place.
- sklearn: Same
- Pandas: Counter({'no_update': 9, 'ValidationError': 1, 'should_update': 1}). The one suggested update looks a bit more extensive than I'd like.



## FGithub errors
# For o1-mini, it returns this error:
# HttpResponseError: (unsupported_value) Unsupported value: 'messages[0].role' does not support 'system' with this model.
# Code: unsupported_value
# Message: Unsupported value: 'messages[0].role' does not support 'system' with this model.

# o1 (first try):
# HttpResponseError: (BadRequest) Model o1 is enabled only for api versions 2024-12-01-preview and later
# Code: BadRequest
# Message: Model o1 is enabled only for api versions 2024-12-01-preview and later

# o1 (second try)
# HttpResponseError: (unsupported_value) Unsupported value: 'messages[0].role' does not support 'system' with this model.
# Code: unsupported_value
# Message: Unsupported value: 'messages[0].role' does not support 'system' with this model.
