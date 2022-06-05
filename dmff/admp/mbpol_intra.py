
import sys
import numpy as np
import jax.numpy as jnp
from jax import grad, value_and_grad
from dmff.settings import DO_JIT
from dmff.utils import jit_condition
from dmff.admp.spatial import v_pbc_shift
from jax import vmap

#const
f5z = 0.999677885
fbasis = 0.15860145369897
fcore = -1.6351695982132
frest = 1.0
reoh = 0.958649;
thetae = 104.3475;
b1 = 2.0;
roh = 0.9519607159623009;
alphaoh = 2.587949757553683;
deohA = 42290.92019288289;
phh1A = 16.94879431193463;
phh2 = 12.66426998162947;

c5zA = jnp.array([4.2278462684916e+04, 4.5859382909906e-02, 9.4804986183058e+03,
       7.5485566680955e+02, 1.9865052511496e+03, 4.3768071560862e+02,
       1.4466054104131e+03, 1.3591924557890e+02,-1.4299027252645e+03,
       6.6966329416373e+02, 3.8065088734195e+03,-5.0582552618154e+02,
      -3.2067534385604e+03, 6.9673382568135e+02, 1.6789085874578e+03,
      -3.5387509130093e+03,-1.2902326455736e+04,-6.4271125232353e+03,
      -6.9346876863641e+03,-4.9765266152649e+02,-3.4380943579627e+03,
       3.9925274973255e+03,-1.2703668547457e+04,-1.5831591056092e+04,
       2.9431777405339e+04, 2.5071411925779e+04,-4.8518811956397e+04,
      -1.4430705306580e+04, 2.5844109323395e+04,-2.3371683301770e+03,
       1.2333872678202e+04, 6.6525207018832e+03,-2.0884209672231e+03,
      -6.3008463062877e+03, 4.2548148298119e+04, 2.1561445953347e+04,
      -1.5517277060400e+05, 2.9277086555691e+04, 2.6154026873478e+05,
      -1.3093666159230e+05,-1.6260425387088e+05, 1.2311652217133e+05,
      -5.1764697159603e+04, 2.5287599662992e+03, 3.0114701659513e+04,
      -2.0580084492150e+03, 3.3617940269402e+04, 1.3503379582016e+04,
      -1.0401149481887e+05,-6.3248258344140e+04, 2.4576697811922e+05,
       8.9685253338525e+04,-2.3910076031416e+05,-6.5265145723160e+04,
       8.9184290973880e+04,-8.0850272976101e+03,-3.1054961140464e+04,
      -1.3684354599285e+04, 9.3754012976495e+03,-7.4676475789329e+04,
      -1.8122270942076e+05, 2.6987309391410e+05, 4.0582251904706e+05,
      -4.7103517814752e+05,-3.6115503974010e+05, 3.2284775325099e+05,
       1.3264691929787e+04, 1.8025253924335e+05,-1.2235925565102e+04,
      -9.1363898120735e+03,-4.1294242946858e+04,-3.4995730900098e+04,
       3.1769893347165e+05, 2.8395605362570e+05,-1.0784536354219e+06,
      -5.9451106980882e+05, 1.5215430060937e+06, 4.5943167339298e+05,
      -7.9957883936866e+05,-9.2432840622294e+04, 5.5825423140341e+03,
       3.0673594098716e+03, 8.7439532014842e+04, 1.9113438435651e+05,
      -3.4306742659939e+05,-3.0711488132651e+05, 6.2118702580693e+05,
      -1.5805976377422e+04,-4.2038045404190e+05, 3.4847108834282e+05,
      -1.3486811106770e+04, 3.1256632170871e+04, 5.3344700235019e+03,
       2.6384242145376e+04, 1.2917121516510e+05,-1.3160848301195e+05,
      -4.5853998051192e+05, 3.5760105069089e+05, 6.4570143281747e+05,
      -3.6980075904167e+05,-3.2941029518332e+05,-3.5042507366553e+05,
       2.1513919629391e+03, 6.3403845616538e+04, 6.2152822008047e+04,
      -4.8805335375295e+05,-6.3261951398766e+05, 1.8433340786742e+06,
       1.4650263449690e+06,-2.9204939728308e+06,-1.1011338105757e+06,
       1.7270664922758e+06, 3.4925947462024e+05,-1.9526251371308e+04,
      -3.2271030511683e+04,-3.7601575719875e+05, 1.8295007005531e+05,
       1.5005699079799e+06,-1.2350076538617e+06,-1.8221938812193e+06,
       1.5438780841786e+06,-3.2729150692367e+03, 1.0546285883943e+04,
      -4.7118461673723e+04,-1.1458551385925e+05, 2.7704588008958e+05,
       7.4145816862032e+05,-6.6864945408289e+05,-1.6992324545166e+06,
       6.7487333473248e+05, 1.4361670430046e+06,-2.0837555267331e+05,
       4.7678355561019e+05,-1.5194821786066e+04,-1.1987249931134e+05,
       1.3007675671713e+05, 9.6641544907323e+05,-5.3379849922258e+05,
      -2.4303858824867e+06, 1.5261649025605e+06, 2.0186755858342e+06,
      -1.6429544469130e+06,-1.7921520714752e+04, 1.4125624734639e+04,
      -2.5345006031695e+04, 1.7853375909076e+05,-5.4318156343922e+04,
      -3.6889685715963e+05, 4.2449670705837e+05, 3.5020329799394e+05,
       9.3825886484788e+03,-8.0012127425648e+05, 9.8554789856472e+04,
       4.9210554266522e+05,-6.4038493953446e+05,-2.8398085766046e+06,
       2.1390360019254e+06, 6.3452935017176e+06,-2.3677386290925e+06,
      -3.9697874352050e+06,-1.9490691547041e+04, 4.4213579019433e+04,
       1.6113884156437e+05,-7.1247665213713e+05,-1.1808376404616e+06,
       3.0815171952564e+06, 1.3519809705593e+06,-3.4457898745450e+06,
       2.0705775494050e+05,-4.3778169926622e+05, 8.7041260169714e+03,
       1.8982512628535e+05,-2.9708215504578e+05,-8.8213012222074e+05,
       8.6031109049755e+05, 1.0968800857081e+06,-1.0114716732602e+06,
       1.9367263614108e+05, 2.8678295007137e+05,-9.4347729862989e+04,
       4.4154039394108e+04, 5.3686756196439e+05, 1.7254041770855e+05,
      -2.5310674462399e+06,-2.0381171865455e+06, 3.3780796258176e+06,
       7.8836220768478e+05,-1.5307728782887e+05,-3.7573362053757e+05,
       1.0124501604626e+06, 2.0929686545723e+06,-5.7305706586465e+06,
      -2.6200352535413e+06, 7.1543745536691e+06,-1.9733601879064e+04,
       8.5273008477607e+04, 6.1062454495045e+04,-2.2642508675984e+05,
       2.4581653864150e+05,-9.0376851105383e+05,-4.4367930945690e+05,
       1.5740351463593e+06, 2.4563041445249e+05,-3.4697646046367e+03,
      -2.1391370322552e+05, 4.2358948404842e+05, 5.6270081955003e+05,
      -8.5007851251980e+05,-6.1182429537130e+05, 5.6690751824341e+05,
      -3.5617502919487e+05,-8.1875263381402e+02,-2.4506258140060e+05,
       2.5830513731509e+05, 6.0646114465433e+05,-6.9676584616955e+05,
       5.1937406389690e+05, 1.7261913546007e+05,-1.7405787307472e+04,
      -3.8301842660567e+05, 5.4227693205154e+05, 2.5442083515211e+06,
      -1.1837755702370e+06,-1.9381959088092e+06,-4.0642141553575e+05,
       1.1840693827934e+04,-1.5334500255967e+05, 4.9098619510989e+05,
       6.1688992640977e+05, 2.2351144690009e+05,-1.8550462739570e+06,
       9.6815110649918e+03,-8.1526584681055e+04,-8.0810433155289e+04,
       3.4520506615177e+05, 2.5509863381419e+05,-1.3331224992157e+05,
      -4.3119301071653e+05,-5.9818343115856e+04, 1.7863692414573e+03,
       8.9440694919836e+04,-2.5558967650731e+05,-2.2130423988459e+04,
       4.4973674518316e+05,-2.2094939343618e+05])

cbasis = jnp.array([6.9770019624764e-04,-2.4209870001642e+01, 1.8113927151562e+01,
       3.5107416275981e+01,-5.4600021126735e+00,-4.8731149608386e+01,
       3.6007189184766e+01, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
      -7.7178474355102e+01,-3.8460795013977e+01,-4.6622480912340e+01,
       5.5684951167513e+01, 1.2274939911242e+02,-1.4325154752086e+02,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00,-6.0800589055949e+00,
       8.6171499453475e+01,-8.4066835441327e+01,-5.8228085624620e+01,
       2.0237393793875e+02, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       3.3525582670313e+02, 7.0056962392208e+01,-4.5312502936708e+01,
      -3.0441141194247e+02, 2.8111438108965e+02, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-1.2983583774779e+02, 3.9781671212935e+01,
      -6.6793945229609e+01,-1.9259805675433e+02, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-8.2855757669957e+02,-5.7003072730941e+01,
      -3.5604806670066e+01, 9.6277766002709e+01, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 8.8645622149112e+02,-7.6908409772041e+01,
       6.8111763314154e+01, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       2.5090493428062e+02,-2.3622141780572e+02, 5.8155647658455e+02,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 2.8919570295095e+03,
      -1.7871014635921e+02,-1.3515667622500e+02, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-3.6965613754734e+03, 2.1148158286617e+02,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00,-1.4795670139431e+03,
       3.6210798138768e+02, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
      -5.3552886800881e+03, 3.1006384016202e+02, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 1.6241824368764e+03, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 4.3764909606382e+03, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 1.0940849243716e+03, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 3.0743267832931e+03, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00])

ccore = jnp.array([2.4332191647159e-02,-2.9749090113656e+01, 1.8638980892831e+01,
      -6.1272361746520e+00, 2.1567487597605e+00,-1.5552044084945e+01,
       8.9752150543954e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
      -3.5693557878741e+02,-3.0398393196894e+00,-6.5936553294576e+00,
       1.6056619388911e+01, 7.8061422868204e+01,-8.6270891686359e+01,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00,-3.1688002530217e+01,
       3.7586725583944e+01,-3.2725765966657e+01,-5.6458213299259e+00,
       2.1502613314595e+01, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       5.2789943583277e+02,-4.2461079404962e+00,-2.4937638543122e+01,
      -1.1963809321312e+02, 2.0240663228078e+02, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-6.2574211352272e+02,-6.9617539465382e+00,
      -5.9440243471241e+01, 1.4944220180218e+01, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-1.2851139918332e+03,-6.5043516710835e+00,
       4.0410829440249e+01,-6.7162452402027e+01, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 1.0031942127832e+03, 7.6137226541944e+01,
      -2.7279242226902e+01, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
      -3.3059000871075e+01, 2.4384498749480e+01,-1.4597931874215e+02,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 1.6559579606045e+03,
       1.5038996611400e+02,-7.3865347730818e+01, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-1.9738401290808e+03,-1.4149993809415e+02,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00,-1.2756627454888e+02,
       4.1487702227579e+01, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
      -1.7406770966429e+03,-9.3812204399266e+01, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-1.1890301282216e+03, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 2.3723447727360e+03, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-1.0279968223292e+03, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 5.7153838472603e+02, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00])

crest = jnp.array([ 0.0000000000000e+00,-4.7430930170000e+00,-1.4422132560000e+01,
      -1.8061146510000e+01, 7.5186735000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
      -2.7962099800000e+02, 1.7616414260000e+01,-9.9741392630000e+01,
       7.1402447000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00,-7.8571336480000e+01,
       5.2434353250000e+01, 7.7696745000000e+01, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       1.7799123760000e+02, 1.4564532380000e+02, 2.2347226000000e+02,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-4.3823284100000e+02,-7.2846553000000e+02,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00,-2.6752313750000e+02, 3.6170310000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00, 0.0000000000000e+00,
       0.0000000000000e+00, 0.0000000000000e+00])

idx1 = jnp.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
       5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7,
       7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6,
       6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9,
       9, 9, 9, 9, 9])

idx2 = jnp.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
       2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4,
       4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2,
       2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4,
       4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1,
       1, 1, 1, 1, 1])
    
idx3 = jnp.array([1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15, 1, 2, 3, 4, 5,
       6, 7, 8, 9,10,11,12,13,14, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,
      12,13, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13, 1, 2, 3, 4, 5,
       6, 7, 8, 9,10,11,12, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12, 1,
       2, 3, 4, 5, 6, 7, 8, 9,10,11, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,
      11, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11, 1, 2, 3, 4, 5, 6, 7, 8,
       9,10, 1, 2, 3, 4, 5, 6, 7, 8, 9,10, 1, 2, 3, 4, 5, 6, 7, 8,
       9,10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9,
       1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2,
       3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6,
       7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3,
       4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2,
       3, 4, 5, 6, 7])

matrix1 = np.zeros((245,16))
matrix2 = np.zeros((245,16))
matrix3 = np.zeros((245,16))
for i in range(245):
    a = int(idx1[i])
    b = int(idx2[i])
    c = int(idx3[i])
    list1 = np.zeros(16)
    list2 = np.zeros(16)
    list3 = np.zeros(16)
    list1[a] = 1
    list2[b] = 1
    list3[c] = 1
    matrix1[i] = list1
    matrix2[i] = list2
    matrix3[i] = list3
    
c5z = jnp.zeros(245)
for i in range(245):
    c5z = c5z.at[i].set(f5z*c5zA[i] + fbasis*cbasis[i]+ fcore*ccore[i] + frest*crest[i])
deoh = f5z*deohA
phh1 = f5z*phh1A*jnp.exp(phh2)
costhe = -0.24780227221366464506

Eh_J = 4.35974434e-18
Na = 6.02214129e+23
kcal_J = 4184.0
c0 = 299792458.0
h_Js = 6.62606957e-34
cal2joule = 4.184
Eh_kcalmol = Eh_J*Na/kcal_J
Eh_cm1 = 1.0e-2*Eh_J/(c0*h_Js)
cm1_kcalmol = Eh_kcalmol/Eh_cm1


## compute intra 
def onebodyenergy(positions, box):
    box_inv = jnp.linalg.inv(box)
    O = positions[::3]
    H1 = positions[1::3]
    H2 = positions[2::3]
    ROH1 = H1 - O
    ROH2 = H2 - O
    RHH = H1 - H2
    ROH1 = v_pbc_shift(ROH1, box, box_inv)
    ROH2 = v_pbc_shift(ROH2, box, box_inv)
    RHH = v_pbc_shift(RHH, box, box_inv)
    dROH1 = jnp.linalg.norm(ROH1, axis=1) 
    dROH2 = jnp.linalg.norm(ROH2, axis=1)
    dRHH = jnp.linalg.norm(RHH, axis=1)
    costh = jnp.sum(ROH1 * ROH2, axis=1) / (dROH1 * dROH2)
    exp1 = jnp.exp(-alphaoh*(dROH1 - roh))
    exp2 = jnp.exp(-alphaoh*(dROH2 - roh))
    Va = deoh*(exp1*(exp1 - 2.0) + exp2*(exp2 - 2.0))
    Vb = phh1*jnp.exp(-phh2*dRHH)
    x1 = (dROH1 - reoh)/reoh
    x2 = (dROH2 - reoh)/reoh
    x3 = costh - costhe
    efac = jnp.exp(-b1*(dROH1 - reoh)**2 + (dROH2 - reoh)**2)
    energy = jnp.sum(onebody_kernel(x1, x2, x3, Va, Vb, efac))
    return energy



@vmap
@jit_condition(static_argnums={})
def onebody_kernel(x1, x2, x3, Va, Vb, efac):      
    const = jnp.array([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    CONST = jnp.array([const,const,const])
    list1 = jnp.array([x1**i for i in range(-1, 15)])
    list2 = jnp.array([x2**i for i in range(-1, 15)])
    list3 = jnp.array([x3**i for i in range(-1, 15)])
    fmat = jnp.array([list1, list2, list3])
    fmat *= CONST
    F1 = jnp.sum(fmat[0].T * matrix1, axis=1) # fmat[0][inI] 1*245
    F2 = jnp.sum(fmat[1].T * matrix2, axis=1) #fmat[1][inJ] 1*245
    F3 = jnp.sum(fmat[0].T * matrix2, axis=1) #fmat[0][inJ] 1*245
    F4 = jnp.sum(fmat[1].T * matrix1, axis=1) #fmat[1][inI] 1*245
    F5 = jnp.sum(fmat[2].T * matrix3, axis=1) #fmat[2][inK] 1*245
    total = c5z * (F1*F2 + F3*F4)* F5
    sum0 = jnp.sum(total[1:245])
    Vc = 2*c5z[0] + efac*sum0
    e1 = Va + Vb + Vc
    e1 += 0.44739574026257
    e1 *= cm1_kcalmol 
    e1 *= cal2joule # conver cal 2 j
    return e1
