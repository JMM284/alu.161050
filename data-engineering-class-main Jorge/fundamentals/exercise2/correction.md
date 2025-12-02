# Fundamentals of Data Engineering – Exercise 2 Correction
### Student: Jorge Moliá

---

## Correction Notes

### Issues to solve:

#### (scrapper) Modify get_songs to use catalog (2 points)
- [ ] Points awarded: 2
- [ ] Comments:

#### (scrapper) Check logs for strange messages (0.5 points)
- [ ] Points awarded: 0
- [ ] Comments: No comments given.

#### (cleaner) Avoid processing catalogs (0.5 points)
- [ ] Points awarded: 0
- [ ] Comments: The code keeps getting the catalog.

#### (Validator) Fix directory creation issue (0.5 points)
- [ ] Points awarded: 0.5
- [ ] Comments:

#### (Validator) Additional validation rule (0.5 points)
- [ ] Points awarded: 0.3
- [ ] Comments: I see you have changed the validation rule, but you should have used the 'utils/chords.py' file to not hardcode the chordes in the rule.

#### Code improvements (0.5 points)
- [ ] Points awarded: 0
- [ ] Comments: Not provided.

### Functionalities to add:

#### 'results' module (0.5 points)
- [ ] Points awarded: 0.2
- [ ] Comments:
- - Your code only prints the results. You are not storing anywhere those results. What if it was a pipeline that needs to be executed daily and you need to track these results to monitor them?
- - You are not logging anything from this module. You could use a log file to both log the execution and the results to keep track.
- - Also, the main process of the module should have been named 'main.py'.

#### 'lyrics' module (2 points)
- [ ] Points awarded: 1.8
- [ ] Comments: Good job. You separated correctly the lyrics and the chords.
- - The main process of the module should have been named 'main.py'.
- - The 'chord' files does not have any sense here and only adds noise to the data.

#### 'insights' module (2 points)
- [ ] Points awarded: 0
- [ ] Comments: Not implemented

#### Main execution file (1 point)
- [ ] Points awarded: 0
- [ ] Comments: Not implemented.

---

## Total Score: 4.8 / 10 points

## General Comments:

Your submission shows good effort in the implemented parts, particularly in the lyrics module where you successfully separated lyrics from chords. However, the exercise is incomplete with several major components missing.

**What Works:**
- Scrapper module functions correctly with catalog integration
- Validator fixes are in place
- Lyrics module has good chord separation logic (1.8/2.0)

**Critical Missing Components:**
- **Insights module**: Not implemented (0/2.0 points lost)
- **Main execution file**: Not implemented (0/1.0 points lost)
- **Cleaner**: Still processes catalog files (0/0.5 points lost)
- **Log analysis**: No comments provided (0/0.5 points lost)
- **Code improvements**: Not provided (0/0.5 points lost)

**Issues in Completed Work:**
- Results module needs proper directory structure (named 'main.py')
- No logging implemented in any module
- Results should be persisted, not just printed
- Chord files in lyrics output add unnecessary noise

**For Future Projects:**
This exercise had a full month timeline with in-class work sessions. Incomplete submissions significantly impact your grade. Prioritize:
1. Completing all required functionalities before adding extra features
2. Testing all modules together in the pipeline
3. Implementing logging for production-ready code
4. Following module structure conventions

The parts you completed show you have the technical skills. Focus on project management and completing all requirements for better results.
