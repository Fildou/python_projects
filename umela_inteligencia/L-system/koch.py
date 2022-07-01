import turtle


def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))


def createLSystem(numIters,axiom):
    startString = axiom
    endString = ""
    for i in range(numIters):
        endString = processString(startString)
        startString = endString

    return endString


def processString(oldStr):  # processing string with set rules
    newstr = ""
    for ch in oldStr:
        newstr = newstr + applyRules(ch)

    return newstr


def applyRules(ch):
    newstr = ""
    if ch == 'F':
        newstr = 'F+F--F+F'   # Rule 1
    else:
        newstr = ch    # no rules apply so keep the character

    return newstr


def drawLsystem(aTurtle, instructions, angle, distance):
    stack = []
    for cmd in instructions:
        aTurtle.pd()    # pen down = drawing
        if cmd == 'F':  # move with drawing
            aTurtle.forward(distance)
        elif cmd == range_char('a', 'u'):   # move without drawing
            aTurtle.pu()    # pen up = not drawing
            aTurtle.forward(distance)
        elif cmd == '+':    # change angle by set value in right direction
            aTurtle.right(angle)
        elif cmd == '|':    # change direction by 180 degrees
            aTurtle.right(180)
        elif cmd == '-':    # change angle by set value in left direction
            aTurtle.left(angle)
        elif cmd == '[':    # save position and angle to stack
            stack.append((aTurtle.position(), aTurtle.heading()))
        elif cmd == ']':    # move to position from stack
            aTurtle.pu()    # pen up = not drawing
            position, heading = stack.pop()    # delete and return position, heading
            aTurtle.goto(position)
            aTurtle.setheading(heading)
    turtle.bye()
