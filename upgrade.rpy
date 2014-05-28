screen upgrade:
    add "Menu/upgrade_back.jpg"

    text '{!s}$'.format(BM.money):
        size 50
        xpos 0.15
        ypos 0.7
        color '090'
        outlines [(1,'000',0,0)]

    imagebutton:
        xpos 1650 ypos 975
        action Return("quit")
        idle "Menu/return.jpg"
        hover "Menu/return_hover.jpg"

    if BM.selected == None:
        $ BM.selected = sunrider
    $ ship = BM.selected

    $ can_use_melee = False
    for weapon in ship.weapons:
        if weapon.wtype == 'Melee':
            $ can_use_melee = True
    $ uses_kinetics = False
    for weapon in ship.weapons:
        if weapon.wtype == 'Kinetic' or weapon.wtype == 'Assault':
            $ uses_kinetics = True
    $ uses_lasers = False
    for weapon in ship.weapons:
        if weapon.wtype == 'Laser' or weapon.wtype == 'Pulse':
            $ uses_lasers = True

    #dictionaries are inherently unsorted, so this is needed ;_;
    $ upgrade_list = []
    $ upgrade_list.append(["BASIC -----------",None,None,None,None])
    $ upgrade_list.append(ship.upgrades['max_hp'])
    $ upgrade_list.append(ship.upgrades['max_en'])
    $ upgrade_list.append(ship.upgrades['evasion'])
#    $ upgrade_list.append(ship.upgrades['move_cost'])  #probably should be set individually in design

    if uses_kinetics:
        $ upgrade_list.append(["KINETIC -----------",None,None,None,None])
        $ upgrade_list.append(ship.upgrades['kinetic_dmg'])
        $ upgrade_list.append(ship.upgrades['kinetic_acc'])
        $ upgrade_list.append(ship.upgrades['kinetic_cost'])

    if uses_lasers:
        $ upgrade_list.append(["LASER -----------",None,None,None,None])
        $ upgrade_list.append(ship.upgrades['energy_dmg'])
        $ upgrade_list.append(ship.upgrades['energy_acc'])
        $ upgrade_list.append(ship.upgrades['energy_cost'])

    if ship.max_missiles > 0:
        $ upgrade_list.append(["MISSILE -----------",None,None,None,None])
        $ upgrade_list.append(ship.upgrades['missile_dmg'])
        $ upgrade_list.append(ship.upgrades['missile_acc'])
        $ upgrade_list.append(ship.upgrades['missile_cost'])
        $ upgrade_list.append(ship.upgrades['max_missiles'])

    if can_use_melee:
        $ upgrade_list.append(["MELEE -----------",None,None,None,None])
        $ upgrade_list.append(ship.upgrades['melee_dmg'])
        $ upgrade_list.append(ship.upgrades['melee_acc'])
        $ upgrade_list.append(ship.upgrades['melee_cost'])

    $ upgrade_list.append(["DEFENSES -----------",None,None,None,None])

    if ship.shield_generation > 0:
        $ upgrade_list.append(ship.upgrades['shield_generation'])
        $ upgrade_list.append(ship.upgrades['shield_range'])

    if ship.flak > 0:
        $ upgrade_list.append(ship.upgrades['flak'])

    $ upgrade_list.append(ship.upgrades['base_armor'])

    if ship.repair > 0:
        $ upgrade_list.append(ship.upgrades['repair'])

    if ship == sunrider:
        add "Menu/upgrade_sunrider.png"
    if ship == blackjack:
        add "Menu/upgrade_blackjack.png"
    if ship == liberty:
        add "Menu/upgrade_liberty.png"
    if ship == phoenix:
        add "Menu/upgrade_phoenix.png"
    if ship == bianca:
        add "Menu/upgrade_bianca.png"

    textbutton 'next ship':
        xpos 0.8
        ypos 0.1
        text_size 50
        text_color 'fff'
        text_outlines [(1,'000',0,0)]
        action Return('next')

    vbox:
        area (40, 270, 1050, 440)

        viewport id "upgrade_list":
            draggable True
            mousewheel True
            scrollbars "vertical"
            child_size (1050,2000)

            vbox:

                for upgrade in upgrade_list:
                    if upgrade[1] == None:
                        add "Menu/upgrade_blank.png"
                    else:
                        add "Menu/upgrade_item.png"

            vbox:
                ypos 10
                xpos 20
                spacing 23

                for upgrade in upgrade_list:
                    if upgrade[1] == None:
                        text upgrade[0]:
                            color '000'
                    else:
                        $ name,level,increase,cost,multiplier = upgrade
                        $ attribute = ""
                        for key in ship.upgrades:
                            if ship.upgrades[key][0] == name:
                                $ attribute = key
                        $ current = getattr(ship,attribute)
                        hbox:
                            spacing 60
                            text name:
                                color '000'
                                min_width 400

                            if increase < 1:
                                text str(current*100)+'% -> '+ str((current+increase)*100)+'%':
                                    color '000'
                                    min_width 200
                            else:
                                text str(current)+' -> '+ str(current+increase):
                                    color '000'
                                    min_width 200

                            text str(level):
                                color '000'
                                min_width 50
                            text str(cost):
                                color '000'
                                min_width 60
                            if BM.money >= cost:
                                textbutton '+':
                                    text_color 'fff'
                                    action Return(attribute)
                                    hovered SetField(BM,'active_upgrade',upgrade)
                                    unhovered SetField(BM,'active_upgrade',None)
                            else:
                                textbutton 'X':
                                    text_color 'c00'
                                    action NullAction()
                                    hovered SetField(BM,'active_upgrade',upgrade)
                                    unhovered SetField(BM,'active_upgrade',None)

      ##show weapon icons and their stats##
    if BM.active_upgrade != None:
        $ name,level,increase,cost,multiplier = BM.active_upgrade
        $ quantifier = ''
        if increase < 1:
            $ type = None
            if name.find('Damage') != -1:
                $ type = 'damage'
                $ quantifier = 'DMG'
            if name.find('Accuracy') != -1:
                $ type = 'accuracy'
                $ quantifier = '%'
            if name.find('Energy Cost') != -1:
                $ type = 'energy_use'
                $ quantifier = 'EN'

            $ count = 0
            for weapon in ship.weapons:
                if name.find( weapon_type(weapon) ) == 0:
                    add weapon.lbl:
                        ypos (750 + count*140)
                        xpos 480
                    frame:
                        background Solid((255,255,255,255))
                        xpos 640
                        ypos (820 + count*140)
                        yanchor 0.5

                        has vbox

                        $ stat = getattr(weapon,type)
                        $ current = int(stat * (1.0+increase*(level-1)) )
                        $ next = int(stat * (1.0+increase * level ))



#                        text weapon.name:
#                            color '000'
                        text str(current)+quantifier+' -> '+ str(next) + quantifier:
                            color '000'

                    $ count += 1

screen store_missile:
    add "Menu/unionstore_missiles.png" xpos 1170 ypos 200

screen store_rocket:
    add "Menu/unionstore_rocket.png" xpos 1170 ypos 200