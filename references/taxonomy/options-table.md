# Taxonomy 选项总表（自动生成，勿手改；改 data/taxonomy.json 后运行 `python3 scripts/ugc_taxonomy.py reindex`）

图片路径相对 skill 根目录，每个选项一张独立图：`assets/options/<category>/<option_id>.webp`（色彩类为色卡）。`look` = 看图提炼的视觉描述（data/visual-descriptors.json）。`N/B/E` = 选项在 Average(normal)/Bold(freak)/Extreme(total) 三档是否可见。

## gender — Gender（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `female` | Female | Female | woman | NBE |  |  | assets/options/gender/female.webp |
| `male` | Male | Male | man | NBE |  |  | assets/options/gender/male.webp |
| `trans_man` | Trans man | Trans man | trans man | NBE |  |  | assets/options/gender/trans_man.webp |
| `trans_woman` | Trans woman | Trans woman | trans woman | NBE |  |  | assets/options/gender/trans_woman.webp |
| `non_binary` | Non-binary | Non-binary person | androgynous non-binary person | NBE |  |  | assets/options/gender/non_binary.webp |

## ethnicity_origin_base — Ethnicity（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `african` | African | African phenotype | African facial features | NBE |  |  | assets/options/ethnicity_origin_base/african.webp |
| `east_asian` | Asian | East Asian supermodel, Korean K-Pop idol phenotype | East Asian facial features, ordinary everyday face (not idol-like) | NBE |  |  | assets/options/ethnicity_origin_base/east_asian.webp |
| `european` | European | European | European facial features | NBE |  |  | assets/options/ethnicity_origin_base/european.webp |
| `indian` | Indian | Indian | South Asian facial features | NBE |  |  | assets/options/ethnicity_origin_base/indian.webp |
| `middle_eastern` | Middle Eastern | Middle Eastern | Middle Eastern facial features, strong brows | NBE |  |  | assets/options/ethnicity_origin_base/middle_eastern.webp |
| `latin_american` | Mixed | Mixed race, Latin American influence | mixed-race Latin American facial features | NBE |  |  | assets/options/ethnicity_origin_base/latin_american.webp |

## age — Age（kind=text, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `adult` | Adult | Adult |  | NBE |  |  | assets/options/age/adult.webp |
| `mature` | Mature | Middle-aged |  | NBE |  |  | assets/options/age/mature.webp |
| `senior` | Senior | Senior |  | NBE |  |  | assets/options/age/senior.webp |

## skin_tone — Skin color（kind=color, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `st_porcelain` | Porcelain | porcelain skin | porcelain pale skin | NBE |  | #f1e2d5 | assets/options/skin_tone/st_porcelain.webp |
| `st_fair` | Fair | fair skin | fair skin | NBE |  | #e8c9b5 | assets/options/skin_tone/st_fair.webp |
| `st_light` | Light | light skin | light skin | NBE |  | #dab49a | assets/options/skin_tone/st_light.webp |
| `st_olive` | Olive | olive skin | olive skin | NBE |  | #b6976e | assets/options/skin_tone/st_olive.webp |
| `st_tan` | Tan | tan skin | tan skin | NBE |  | #bc8e67 | assets/options/skin_tone/st_tan.webp |
| `st_brown` | Brown | brown skin | brown skin | NBE |  | #805135 | assets/options/skin_tone/st_brown.webp |
| `st_deep` | Deep brown | deep brown skin | deep brown skin | NBE |  | #543621 | assets/options/skin_tone/st_deep.webp |
| `st_ebony` | Ebony | ebony skin | dark ebony skin | NBE |  | #2d211b | assets/options/skin_tone/st_ebony.webp |

## height — Height（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `h_average` | Average | average height | average height | NBE |  |  | assets/options/height/h_average.webp |
| `h_tall` | Tall | tall | tall, long-legged | NBE |  |  | assets/options/height/h_tall.webp |
| `h_very_tall` | Very tall | very tall | extremely tall and towering, head near the top of the frame | NBE |  |  | assets/options/height/h_very_tall.webp |

## body_type — Build（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `body_slim` | Slim | slim build | very thin narrow frame | NBE |  |  | assets/options/body_type/body_slim.webp |
| `body_athletic` | Athletic | athletic build | lean athletic frame | NBE |  |  | assets/options/body_type/body_athletic.webp |
| `body_muscular` | Muscular | muscular build | broad muscular frame, thick arms and chest | NBE |  |  | assets/options/body_type/body_muscular.webp |
| `body_curvy` | Curvy | curvy build | hourglass curvy figure | NBE |  |  | assets/options/body_type/body_curvy.webp |
| `body_heavy` | Heavy | heavy build | heavy round build with a large belly | NBE |  |  | assets/options/body_type/body_heavy.webp |
| `body_ultra` | Ultra Muscular | extreme muscular build | absurdly hyper-muscular bodybuilder torso and arms on an ordinary head | NBE |  |  | assets/options/body_type/body_ultra.webp |

## proportions — Proportions（kind=media, max=2）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `pr_longlimbs` | Long limbs | long limbs | extra-long legs and arms | NBE |  |  | assets/options/proportions/pr_longlimbs.webp |
| `pr_shortlegs` | Short legs | short legs | noticeably short legs, long torso | NBE |  |  | assets/options/proportions/pr_shortlegs.webp |
| `pr_shoulders` | Broad shoulders | broad shoulders | very broad shoulders | NBE |  |  | assets/options/proportions/pr_shoulders.webp |
| `pr_waist` | Tiny waist | tiny waist | tiny cinched waist | NBE |  |  | assets/options/proportions/pr_waist.webp |
| `pr_egg` | Egg body | egg-shaped body | egg-shaped body: wide round hips and balloon trousers tapering to skinny ankles | -BE |  |  | assets/options/proportions/pr_egg.webp |
| `pr_potbelly` | Pot belly | pot belly | round pot belly pushing out a buttoned waistcoat | -BE |  |  | assets/options/proportions/pr_potbelly.webp |

## freak_head — Head shape（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `head_oval` | Standard | oval face | balanced oval face | NBE |  |  | assets/options/freak_head/head_oval.webp |
| `head_long` | Long | long face | long elongated face | NBE |  |  | assets/options/freak_head/head_long.webp |
| `head_tiny` | Tiny | tiny head | comically tiny head on a normal-sized body | -BE |  |  | assets/options/freak_head/head_tiny.webp |
| `head_forehead` | High forehead | high forehead | very high domed forehead | -BE |  |  | assets/options/freak_head/head_forehead.webp |
| `head_ancient` | Caveman | caveman-like head | heavy caveman-like brow ridge and broad flat nose | --E |  |  | assets/options/freak_head/head_ancient.webp |
| `head_herojaw` | Gigachad | sharp heroic jawline | massively wide chiseled comic-hero jaw | --E |  |  | assets/options/freak_head/head_herojaw.webp |
| `head_megachin` | Mega jaw | oversized chin | huge oversized chin and jowls | --E |  |  | assets/options/freak_head/head_megachin.webp |
| `head_round` | Round | round face | round chubby face | NBE |  |  | assets/options/freak_head/head_round.webp |
| `head_square` | Square | square face | blocky square face and jaw | NBE |  |  | assets/options/freak_head/head_square.webp |
| `head_heart` | Heart | heart-shaped face | heart-shaped face with a pointed chin | NBE |  |  | assets/options/freak_head/head_heart.webp |

## freak_neck — Neck（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `neck_normal` | Standard | normal neck | normal neck | NBE |  |  | assets/options/freak_neck/neck_normal.webp |
| `neck_column` | Column | column-like neck | thick column-like neck as wide as the head | -BE |  |  | assets/options/freak_neck/neck_column.webp |
| `neck_long` | Long | long neck | conspicuously long swan-like neck | -BE |  |  | assets/options/freak_neck/neck_long.webp |
| `neck_short` | Short | short neck | very short neck, head sitting low on the shoulders | NBE |  |  | assets/options/freak_neck/neck_short.webp |

## eye_shape — Eye shape（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `es_almond` | Almond | almond eyes | almond-shaped eyes | NBE |  |  | assets/options/eye_shape/es_almond.webp |
| `es_round` | Round | round eyes | round open eyes | NBE |  |  | assets/options/eye_shape/es_round.webp |
| `es_monolid` | Monolid | monolid eyes | monolid eyes | NBE |  |  | assets/options/eye_shape/es_monolid.webp |
| `es_close` | Close-set | close-set eyes | close-set eyes | -BE |  |  | assets/options/eye_shape/es_close.webp |
| `es_wide` | Wide-set | wide-set eyes | very wide-set eyes | -BE |  |  | assets/options/eye_shape/es_wide.webp |
| `es_uneven` | Uneven | uneven eyes | slightly uneven eyes, one smaller | -BE |  |  | assets/options/eye_shape/es_uneven.webp |
| `es_large` | Large | large eyes | large bright eyes | NBE |  |  | assets/options/eye_shape/es_large.webp |
| `es_huge` | Huge | huge eyes | enormous cartoonishly huge eyes with giant irises | -BE |  |  | assets/options/eye_shape/es_huge.webp |
| `es_hooded` | Hooded | hooded eyes | hooded eyes | NBE |  |  | assets/options/eye_shape/es_hooded.webp |
| `es_upturned` | Upturned | upturned eyes | upturned cat-like eyes | NBE |  |  | assets/options/eye_shape/es_upturned.webp |
| `es_downturned` | Downturned | downturned eyes | droopy downturned eyes | NBE |  |  | assets/options/eye_shape/es_downturned.webp |

## eye_color — Eye color（kind=color, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `eye_black` | Black | black eyes |  | NBE |  | #191615 | assets/options/eye_color/eye_black.webp |
| `eye_brown` | Brown | brown eyes |  | NBE |  | #67432c | assets/options/eye_color/eye_brown.webp |
| `eye_hazel` | Hazel | hazel eyes |  | NBE |  | #887546 | assets/options/eye_color/eye_hazel.webp |
| `eye_green` | Green | green eyes |  | NBE |  | #648254 | assets/options/eye_color/eye_green.webp |
| `eye_blue` | Blue | blue eyes |  | NBE |  | #5182a1 | assets/options/eye_color/eye_blue.webp |
| `eye_ice_blue` | Ice blue | ice blue eyes |  | NBE |  | #a5cbd6 | assets/options/eye_color/eye_ice_blue.webp |
| `eye_amber` | Amber | amber eyes |  | NBE |  | #bd8c45 | assets/options/eye_color/eye_amber.webp |
| `eye_grey` | Grey | grey eyes |  | NBE |  | #939b9d | assets/options/eye_color/eye_grey.webp |

## freak_face — Features（kind=media, max=4）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `fn_freckles` | Freckles | freckles | dense freckles across nose and cheeks | NBE | marks |  | assets/options/freak_face/fn_freckles.webp |
| `fn_dimples` | Dimples | dimples | deep cheek dimples | NBE | cheeks |  | assets/options/freak_face/fn_dimples.webp |
| `fn_eyebags` | Heavy eye bags | heavy eye bags | heavy dark under-eye bags | NBE | eyes |  | assets/options/freak_face/fn_eyebags.webp |
| `ff_marks_12` | Blush | rosy blush | round doll-like pink blush circles on the cheeks | -BE | marks |  | assets/options/freak_face/ff_marks_12.webp |
| `fn_cheekbones` | High cheekbones | high cheekbones | razor-sharp hollow cheekbones | NBE | cheeks |  | assets/options/freak_face/fn_cheekbones.webp |
| `fn_fulllips` | Full lips | full lips | very full glossy lips | NBE | lips |  | assets/options/freak_face/fn_fulllips.webp |
| `fn_thickbrows` | Thick brows | thick eyebrows | thick bushy dark eyebrows | NBE | brows |  | assets/options/freak_face/fn_thickbrows.webp |
| `fn_mole` | Beauty mark | beauty mark | small dark beauty mark above the lip | NBE | marks |  | assets/options/freak_face/fn_mole.webp |
| `ff_nose_0` | Potato nose | potato nose | big bulbous red potato nose | -BE | nose |  | assets/options/freak_face/ff_nose_0.webp |
| `ff_nose_1` | Button nose | button nose | small upturned button nose | -BE | nose |  | assets/options/freak_face/ff_nose_1.webp |
| `ff_nose_2` | Long pointy nose | long pointy nose | long sharp pointy nose | -BE | nose |  | assets/options/freak_face/ff_nose_2.webp |
| `fn_tinynose` | Tiny nose | tiny nose | tiny delicate nose | NBE | nose |  | assets/options/freak_face/fn_tinynose.webp |
| `ff_lips_3` | Pouty lips | pouty lips | exaggerated pouty puckered lips | -BE | lips |  | assets/options/freak_face/ff_lips_3.webp |
| `ff_lips_4` | Tiny pursed mouth | tiny pursed mouth | tiny pursed little mouth | -BE | lips |  | assets/options/freak_face/ff_lips_4.webp |
| `fn_widemouth` | Wide mouth | wide mouth | very wide thin mouth | NBE | lips |  | assets/options/freak_face/fn_widemouth.webp |
| `ff_brows_5` | Unibrow | unibrow | thick dark unibrow | -BE | brows |  | assets/options/freak_face/ff_brows_5.webp |
| `ff_brows_6` | Thin high brows | thin high brows | pencil-thin highly arched 1920s brows | -BE | brows |  | assets/options/freak_face/ff_brows_6.webp |
| `ff_brows_7` | Brush brows | brush brows | wild bushy upward-brushed brows | -BE | brows |  | assets/options/freak_face/ff_brows_7.webp |
| `ff_ears_8` | Jug ears | jug ears | big protruding jug ears | -BE | ears |  | assets/options/freak_face/ff_ears_8.webp |
| `ff_ears_9` | Uneven ears | uneven ears | mismatched uneven ears | -BE | ears |  | assets/options/freak_face/ff_ears_9.webp |
| `ff_teeth_10` | Gap teeth | gap teeth | wide gap between the front teeth | -BE | teeth |  | assets/options/freak_face/ff_teeth_10.webp |
| `ff_teeth_11` | Buck teeth | buck teeth | prominent buck teeth resting on the lower lip | -BE | teeth |  | assets/options/freak_face/ff_teeth_11.webp |
| `fn_pointychin` | Pointy chin | pointy chin | sharp pointed chin | NBE | chin |  | assets/options/freak_face/fn_pointychin.webp |
| `ff_chin_13` | Weak chin | weak chin | weak receding chin | -BE | chin |  | assets/options/freak_face/ff_chin_13.webp |
| `ff_forehead_14` | Big forehead | big forehead | huge high forehead with a receding hairline | -BE | forehead |  | assets/options/freak_face/ff_forehead_14.webp |

## facial_hair — Facial hair（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `fh_none` | Clean-shaven | clean-shaven | clean-shaven | NBE |  |  | assets/options/facial_hair/fh_none.webp |
| `fh_stubble` | Stubble | stubble | scruffy uneven stubble | NBE |  |  | assets/options/facial_hair/fh_stubble.webp |
| `fh_beard` | Full beard | full beard | full thick bushy beard | NBE |  |  | assets/options/facial_hair/fh_beard.webp |
| `fh_goatee` | Goatee | goatee | long thin pointed goatee | NBE |  |  | assets/options/facial_hair/fh_goatee.webp |
| `fh_moustache` | Moustache | moustache | thick 70s horseshoe moustache | NBE |  |  | assets/options/facial_hair/fh_moustache.webp |
| `fh_pencil` | Pencil moustache | pencil moustache | thin pencil moustache | NBE |  |  | assets/options/facial_hair/fh_pencil.webp |
| `fh_pushbroom` | Push-broom moustache | push-broom moustache | enormous walrus push-broom moustache | -BE |  |  | assets/options/facial_hair/fh_pushbroom.webp |
| `fh_braid` | Braided beard | braided beard | long viking beard with two braids | -BE |  |  | assets/options/facial_hair/fh_braid.webp |

## hair — Hairstyle（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `hs_lampshade` | Lampshade bob | lampshade bob | rigid lampshade bob flaring out stiffly at the jaw with a blunt fringe | -BE |  |  | assets/options/hair/hs_lampshade.webp |
| `hair_bald` | Bald | bald | smooth shaved bald head | NBE |  |  | assets/options/hair/hair_bald.webp |
| `hair_buzz` | Buzz cut | buzz cut | very short bleached-style buzz cut | NBE |  |  | assets/options/hair/hair_buzz.webp |
| `hair_bowl` | Bowl cut | bowl cut | perfectly round glossy helmet bowl cut with a straight fringe | NBE |  |  | assets/options/hair/hair_bowl.webp |
| `hair_mullet` | Mullet | mullet | curly 80s mullet, short top and long wavy back | NBE |  |  | assets/options/hair/hair_mullet.webp |
| `hair_braids` | Braids | braids | long box braids with gold cuffs | NBE |  |  | assets/options/hair/hair_braids.webp |
| `hair_pigtails` | Pigtails | pigtails | two high pigtails with a blunt fringe | NBE |  |  | assets/options/hair/hair_pigtails.webp |
| `hair_afro` | Afro | afro | huge perfectly round afro | NBE |  |  | assets/options/hair/hair_afro.webp |
| `hair_punk` | Mohawk | mohawk | tall spiky mohawk on shaved sides | NBE |  |  | assets/options/hair/hair_punk.webp |
| `hs_pompadour` | Volume waves | volume waves | huge voluminous 70s feathered blow-out waves | -BE |  |  | assets/options/hair/hs_pompadour.webp |
| `hs_beehive` | Beehive | beehive | towering 60s beehive | -BE |  |  | assets/options/hair/hs_beehive.webp |
| `hs_dome` | Perm | perm | tight curly perm | -BE |  |  | assets/options/hair/hs_dome.webp |
| `hair_long` | Long hair | long hair | very long straight centre-parted hair past the chest | NBE |  |  | assets/options/hair/hair_long.webp |
| `hair_short` | Short hair | short hair | neat short cropped hair | NBE |  |  | assets/options/hair/hair_short.webp |
| `hs_horns` | Hair horns | hair horns | hair sculpted into two glossy curved devil horns | -BE |  |  | assets/options/hair/hs_horns.webp |
| `hs_softserve` | Soft-serve swirl | soft-serve swirl hair | hair piled into a tall soft-serve ice-cream swirl | -BE |  |  | assets/options/hair/hs_softserve.webp |
| `hs_sphere` | Curl sphere | curl sphere hair | giant tight-curl sphere of hair | -BE |  |  | assets/options/hair/hs_sphere.webp |
| `hs_mouse` | Mouse-ear puffs | mouse-ear puffs | two round bun puffs like mouse ears | -BE |  |  | assets/options/hair/hs_mouse.webp |
| `hs_wings` | Hair wings | hair wings | hair teased out sideways into two big fluffy wings | -BE |  |  | assets/options/hair/hs_wings.webp |
| `hs_hedgehog` | Hedgehog spikes | hedgehog spikes | spiky hedgehog spikes radiating out, frosted tips | -BE |  |  | assets/options/hair/hs_hedgehog.webp |
| `hs_tufts` | Bald + side tufts | bald with side tufts | bald crown with two wild side tufts | -BE |  |  | assets/options/hair/hs_tufts.webp |
| `hs_stairs` | Stair steps | stair-step hair | flat-top hair cut into a staircase of steps | -BE |  |  | assets/options/hair/hs_stairs.webp |
| `hs_shelf` | Shelf bob | shelf bob | straight bob with one side jutting out horizontally like a shelf | -BE |  |  | assets/options/hair/hs_shelf.webp |
| `hs_corkscrews` | Twin corkscrews | twin corkscrews | two tall twisted corkscrew horns of hair | -BE |  |  | assets/options/hair/hs_corkscrews.webp |
| `hs_sidecoil` | Side coil | side coil | single giant coiled bun on one side of the head | -BE |  |  | assets/options/hair/hs_sidecoil.webp |
| `hs_mushroom` | Mushroom bowl | mushroom bowl | wide mushroom-cap bowl cut | -BE |  |  | assets/options/hair/hs_mushroom.webp |

## hair_colour — Hair Color（kind=color, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `hc_black` | Jet black | jet black hair |  | NBE |  | #151515 | assets/options/hair_colour/hc_black.webp |
| `hc_darkbrown` | Dark brown | dark brown hair |  | NBE |  | #39281f | assets/options/hair_colour/hc_darkbrown.webp |
| `hc_chestnut` | Chestnut | chestnut hair |  | NBE |  | #794a33 | assets/options/hair_colour/hc_chestnut.webp |
| `hc_ginger` | Ginger | ginger hair |  | NBE |  | #b56131 | assets/options/hair_colour/hc_ginger.webp |
| `hc_red` | Red | red hair |  | NBE |  | #b43636 | assets/options/hair_colour/hc_red.webp |
| `hc_blonde` | Blonde | blonde hair |  | NBE |  | #d9b774 | assets/options/hair_colour/hc_blonde.webp |
| `hc_platinum` | Platinum | platinum hair |  | NBE |  | #e4d9bc | assets/options/hair_colour/hc_platinum.webp |
| `hc_grey` | Grey | grey hair |  | NBE |  | #8c8c8c | assets/options/hair_colour/hc_grey.webp |
| `hc_white` | White | white hair |  | NBE |  | #eee9dd | assets/options/hair_colour/hc_white.webp |
| `hc_pink` | Pastel pink | pastel pink hair |  | NBE |  | #dd9ab7 | assets/options/hair_colour/hc_pink.webp |
| `hc_lilac` | Lilac | lilac hair |  | NBE |  | #b0a0ce | assets/options/hair_colour/hc_lilac.webp |
| `hc_blue` | Blue | blue hair |  | NBE |  | #4080bb | assets/options/hair_colour/hc_blue.webp |
| `hc_green` | Green | green hair |  | NBE |  | #548060 | assets/options/hair_colour/hc_green.webp |

## distinctive — Distinctive features（kind=media, max=2）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `df_hetero` | Odd eyes | heterochromia (odd eyes) | heterochromia: one blue eye, one brown eye | NBE |  |  | assets/options/distinctive/df_hetero.webp |
| `df_facetattoo` | Face tattoo | face tattoo | small scattered face tattoos | NBE |  |  | assets/options/distinctive/df_facetattoo.webp |
| `df_septum` | Piercing | septum piercing | septum ring piercing | NBE |  |  | assets/options/distinctive/df_septum.webp |
| `df_ears` | Stacked ear piercings | stacked ear piercings | ear cartilage stacked with many rings | NBE |  |  | assets/options/distinctive/df_ears.webp |
| `df_slits` | Brow slits | brow slits | shaved slits in one eyebrow | NBE |  |  | assets/options/distinctive/df_slits.webp |
| `df_bleached` | Bleached | bleached brows | bleached near-white eyebrows | NBE |  |  | assets/options/distinctive/df_bleached.webp |
| `df_nobrows` | No brows | no brows | no eyebrows at all | NBE |  |  | assets/options/distinctive/df_nobrows.webp |
| `df_grill` | Gold grill | gold grill teeth | full gold grill on the teeth | NBE |  |  | assets/options/distinctive/df_grill.webp |
| `df_braces` | Braces | braces | metal braces | NBE |  |  | assets/options/distinctive/df_braces.webp |
| `df_scar` | Brow scar | brow scar | scar cutting through one eyebrow | NBE |  |  | assets/options/distinctive/df_scar.webp |
| `df_gems` | Face gems | face gems | colourful face gems and rhinestones under the eyes | NBE |  |  | assets/options/distinctive/df_gems.webp |
| `df_elf` | Elf ears | elf ears | long pointed elf ears | NBE |  |  | assets/options/distinctive/df_elf.webp |
| `df_lashes` | Big lashes | big lashes | huge dramatic doll lashes | NBE |  |  | assets/options/distinctive/df_lashes.webp |
| `df_bandage` | Nose tape | nose tape | white strip of tape across the nose bridge | NBE |  |  | assets/options/distinctive/df_bandage.webp |

## aesthetic — Style（kind=media, max=1）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `retro` | Retro | retro outfit | head-to-toe mustard 70s suit with wide lapels and flared trousers, patterned shirt | NBE |  |  | assets/options/aesthetic/retro.webp |
| `sporty` | Sporty | sporty outfit | shiny purple-teal 90s windbreaker tracksuit, headband, chunky white trainers | NBE |  |  | assets/options/aesthetic/sporty.webp |
| `y2k` | Y2K | Y2K fashion | all-pink velour Y2K tracksuit, tinted small sunglasses | NBE |  |  | assets/options/aesthetic/y2k.webp |
| `theatrical` | Theatre | theatrical costume | Elizabethan costume: huge white ruff collar, velvet doublet, long red cape | NBE |  |  | assets/options/aesthetic/theatrical.webp |
| `goth` | Goth | goth outfit | floor-length black gothic coat, platform boots, severe black fringe | NBE |  |  | assets/options/aesthetic/goth.webp |
| `suits` | Suits | formal suit | slim black two-piece suit, white shirt, skinny black tie | NBE |  |  | assets/options/aesthetic/suits.webp |
| `streetstyle` | Streetstyle | streetstyle outfit | bright orange puffer jacket, beanie, cargo trousers, cross-body bag | NBE |  |  | assets/options/aesthetic/streetstyle.webp |
| `casual` | Casual | casual outfit | plain white tee, light-wash jeans, belt bag, sandals with socks | NBE |  |  | assets/options/aesthetic/casual.webp |

## accessory — Accessories（kind=media, max=3）

| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |
|---|---|---|---|---|---|---|---|
| `acc_none` | None | no accessories | no accessories | NBE |  |  | assets/options/accessory/acc_none.webp |
| `acc_glasses` | Glasses | wearing glasses | rimless glasses | NBE |  |  | assets/options/accessory/acc_glasses.webp |
| `acc_headphones` | Headphones | wearing headphones | large black over-ear headphones | NBE |  |  | assets/options/accessory/acc_headphones.webp |
| `acc_jewelry` | Jewelry | wearing jewelry | layered silver chain necklaces | NBE |  |  | assets/options/accessory/acc_jewelry.webp |
| `acc_hat` | Hat | wearing a hat | faded black baseball cap | NBE |  |  | assets/options/accessory/acc_hat.webp |
| `acc_bag` | Bag | carrying a bag | brown suede top-handle bag | NBE |  |  | assets/options/accessory/acc_bag.webp |
