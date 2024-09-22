

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