
##### HAWK DOVE GAME

HAWK_DOVE_TEXT = """
<html>
    <body>
        <p>
            The <b>Hawk-Dove game</b> is a classical model in evolutionary biology 
            that explores how individuals in a population adopt different strategies 
            when competing for limited resources. The game is often used to study 
            the evolution of aggression and conflict.
        </p>
        <p>
            In this game, two strategies are possible:
            <ul>
                <li><b>Hawk:</b> Aggressive strategy. Always fights for the resource, 
                    risking injury if the opponent also fights.</li>
                <li><b>Dove:</b> Peaceful strategy. Avoids conflict; if the opponent is a Hawk, 
                    the Dove yields and escapes unharmed. If facing another Dove, they share the resource.</li>
            </ul>
        </p>
        <p>
            The outcome depends on two parameters: the <b>value</b> of the resource 
            (<i>V</i>) and the <b>cost</b> of an injury from fighting (<i>C</i>). 
            The payoff to the individual in the row, against an opponent in the column, is:
        </p>
        <table border="1" cellpadding="6" cellspacing="0" align="center">
            <tr>
                <th></th>
                <th>vs Hawk</th>
                <th>vs Dove</th>
            </tr>
            <tr>
                <td><b>Hawk</b></td>
                <td align="center">(<i>V</i> &minus; <i>C</i>) / 2</td>
                <td align="center"><i>V</i></td>
            </tr>
            <tr>
                <td><b>Dove</b></td>
                <td align="center">0</td>
                <td align="center"><i>V</i> / 2</td>
            </tr>
        </table>
        <ul>
            <li>Hawk vs Hawk: each wins half the time and pays the cost when it loses, 
                so the average payoff is (<i>V</i> &minus; <i>C</i>) / 2</li>
            <li>Hawk vs Dove: the Hawk takes the whole resource, <i>V</i>; the Dove gets 0</li>
            <li>Dove vs Dove: they share the resource, <i>V</i> / 2 each</li>
        </ul>
        <p>
            Let <i>p</i> be the fraction of Hawks in the population. The average payoff 
            of each strategy is:
        </p>
        <p align="center">
            <i>E</i>(Hawk) = <i>p</i> &middot; (<i>V</i> &minus; <i>C</i>) / 2 + (1 &minus; <i>p</i>) &middot; <i>V</i>
            <br>
            <i>E</i>(Dove) = (1 &minus; <i>p</i>) &middot; <i>V</i> / 2
        </p>
        <p>
            Over time, the frequencies of Hawks and Doves in a population reach an 
            <b>evolutionarily stable strategy (ESS)</b>, where no individual can improve 
            its fitness by unilaterally changing strategy.
        </p>
        <ul>
            <li>If <i>V</i> &ge; <i>C</i>, fighting is always worth the risk, 
                so Hawks take over the whole population (<i>p</i>* = 1).</li>
            <li>If <i>C</i> &gt; <i>V</i>, neither strategy wins outright. Setting 
                <i>E</i>(Hawk) = <i>E</i>(Dove) and solving for <i>p</i> gives a stable mix:
                <p align="center"><b><i>p</i>* = <i>V</i> / <i>C</i></b></p>
                Hawks are favored when they are rarer than <i>p</i>*, and Doves are favored when 
                Hawks are more common than <i>p</i>*, so the population is pulled back toward 
                <i>p</i>*.</li>
        </ul>
        <p>
            This model illustrates how aggression and cooperation can coexist in populations, 
            and is a foundational example in <i>evolutionary game theory</i>.
        </p>
    </body>
</html>
"""


HAWK_DOVE_LABEL = "Hawk-Dove Evolutionary Game"
HAWK_DOVE_WIKI = '<a href="https://en.wikipedia.org/wiki/Hawk–dove_game">Hawk-Dove Game Wikipedia</a>'




APP_WINDOW_WIDTH = 900
APP_WINDOW_HEIGHT = 900








#### LOTKA VOLTERRA

LOTKA_VOLTERRA_TEXT = """
<html>
    <body>
        <p>
            The <b>Lotka–Volterra model</b> is a fundamental mathematical model in ecology 
            that describes the dynamics of biological systems in which two species interact, 
            typically a predator and its prey.
        </p>
        <p>
            The classic model consists of two coupled differential equations:
            <ul>
                <li><b>Prey population:</b> grows exponentially in the absence of predators, 
                    but decreases due to predation.</li>
                <li><b>Predator population:</b> depends on the availability of prey for survival, 
                    and declines when prey is scarce.</li>
            </ul>
        </p>
        <p>
            The interactions produce <b>cyclical dynamics</b>:
            <ul>
                <li>When prey numbers increase, predators have more food and their population rises.</li>
                <li>As predator numbers rise, they consume more prey, causing prey population to decline.</li>
                <li>With fewer prey, predators starve and their numbers decrease, allowing prey to recover.</li>
            </ul>
        </p>
        <p>
            The Lotka–Volterra model is an idealized system and assumes:
            <ul>
                <li>No other food sources for the predator</li>
                <li>Unlimited resources for the prey except predation</li>
                <li>Constant interaction rates between predator and prey</li>
            </ul>
        </p>
        <p>
            Despite its simplicity, the model is foundational in population ecology, 
            helping scientists understand oscillations, stability, and the effects of 
            species interactions on ecosystems.
        </p>
    </body>
</html>
"""


LOTKA_VOLTERRA_LABEL = "Lotka-Volterra Population Game"
LOTKA_VOLTERRA_WIKI = '<a href="https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations">Lotka Volterra Wikipedia</a>'